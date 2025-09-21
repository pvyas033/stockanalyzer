from mcp.server.fastmcp import FastMCP
import yfinance as yf
import feedparser
import urllib.parse   
import os
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np

load_dotenv()

mcp = FastMCP("Stock Server")

def safe_format(value, digits=2):
    return f"{value:.{digits}f}" if value is not None else "N/A"

def gemini_llm_call(prompt: str) -> str:
    """
    Call Gemini model with a prompt and return text response.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-001')
    response = model.generate_content(prompt)
    return response.text.strip()

def fetch_latest_news(query="stock market India"):
    # Encode query so spaces/special chars are safe in URLs
    encoded_query = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries[:20]:  # Limit to latest 20
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })
    return articles

def currency_symbol_for_symbol(symbol):
    if symbol.endswith('.NS') or symbol.endswith('.BO'):
        return "₹"
    return "$"

def get_stock_price_internal(symbol: str) -> dict:
    """
    Internal helper to fetch stock price using yfinance.
    Returns a dict with 'price' and 'message'.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")
        csymbol = currency_symbol_for_symbol(symbol)

        if not data.empty:
            price = data['Close'].iloc[-1]
            return {
                "price": float(price),
                "message": f"The current price of {symbol} is: {csymbol}{price:.2f}"
            }
        else:
            info = ticker.info
            price = info.get("regularMarketPrice")
            if price is not None:
                return {
                    "price": float(price),
                    "message": f"The current price of {symbol} is: {csymbol}{price:.2f}"
                }
    except Exception as e:
        return {"price": None, "message": f"Error fetching price for {symbol}: {str(e)}"}

    # fallback if everything fails
    return {"price": None, "message": f"No data available for {symbol}"}


@mcp.tool()
def get_stock_price(symbol: str) -> str:
    """
    Get stock price

    Parameters:
        symbol: stock ticker symbol

    Returns:
        stock price message as string
    """
    return get_stock_price_internal(symbol)["message"]


@mcp.tool()
def compare_stocks(symbol1: str, symbol2: str) -> str:
    result1 = get_stock_price_internal(symbol1)
    result2 = get_stock_price_internal(symbol2)

    price1 = result1.get("price")
    price2 = result2.get("price")

    if price1 is None or price2 is None:
        return f"Could not get stock price for {symbol1} or {symbol2}.\n{result1['message']}\n{result2['message']}"

    curr1 = currency_symbol_for_symbol(symbol1)
    curr2 = currency_symbol_for_symbol(symbol2)

    # If currencies differ, just report prices without numeric comparison
    if curr1 != curr2:
        return (f"{symbol1} price: {curr1}{price1:.2f}\n"
                f"{symbol2} price: {curr2}{price2:.2f}\n"
                "Prices are in different currencies and cannot be directly compared.")

    # Compare when same currency
    if price1 > price2:
        return f"{symbol1} ({curr1}{price1:.2f}) is higher than {symbol2} ({curr2}{price2:.2f})"
    elif price1 < price2:
        return f"{symbol2} ({curr2}{price2:.2f}) is higher than {symbol1} ({curr1}{price1:.2f})"
    else:
        return f"Both {symbol1} and {symbol2} have the same price ({curr1}{price1:.2f})"


@mcp.tool()
def analyze_stock(symbol: str, trade_type: str = "intraday") -> str:
    """
    Analyze whether to buy a company's stock today for intraday or delivery trading.

    Parameters:
        symbol: stock ticker (e.g., "AAPL", "RELIANCE.NS")
        trade_type: "intraday" or "delivery"

    Returns:
        Recommendation string: Yes/No with reasoning.
    """
    # 1. Get stock data
    ticker = yf.Ticker(symbol)
    if trade_type == "intraday":
        data = ticker.history(period="1d", interval="1h")
    else:
        data = ticker.history(period="1mo", interval="1d")

    if data.empty:
        return f"No price data available for {symbol}"

    # 2. Calculate technical indicators
    close_prices = data['Close']

    # Moving Averages
    ma5 = close_prices.rolling(window=5).mean().iloc[-1]
    ma10 = close_prices.rolling(window=10).mean().iloc[-1] if len(close_prices) >= 10 else None
    ma20 = close_prices.rolling(window=20).mean().iloc[-1] if len(close_prices) >= 20 else None
    ma50 = close_prices.rolling(window=50).mean().iloc[-1] if len(close_prices) >= 50 else None

    # RSI (14-day)
    delta = close_prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=14).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs.iloc[-1])) if loss.iloc[-1] != 0 else 100

    indicators = {
        "MA5": ma5,
        "MA10": ma10,
        "MA20": ma20,
        "MA50": ma50,
        "RSI": rsi
    }

    # 3. Fetch news
    articles = fetch_latest_news(f"{symbol} stock")
    news_texts = [a["title"] for a in articles] if articles else []

    # 4. Build prompt for Gemini
    prompt = f"""
    You are a financial analyst.
    Analyze whether to BUY this stock today for {trade_type.upper()} trading.

    Stock Symbol: {symbol}
    Recent Technical Indicators:
    - MA5: {safe_format(ma5)}
    - MA10: {safe_format(ma10)}
    - MA20: {safe_format(ma20)}
    - MA50: {safe_format(ma50)}
    - RSI (14): {safe_format(rsi)}

    Recent News Headlines: {news_texts}

    Rules:
    - RSI > 70 → Overbought (Sell signal)
    - RSI < 30 → Oversold (Buy signal)
    - If short MAs > long MAs → Uptrend
    - Weigh news sentiment alongside technicals.

    Respond with a clear YES or NO, followed by a short reasoning.
    """

    # 5. Call Gemini
    response = gemini_llm_call(prompt)
    return response
    """
    Analyze whether to buy a company's stock today for intraday or delivery trading.

    Parameters:
        symbol: stock ticker (e.g., "AAPL", "RELIANCE.NS")
        trade_type: "intraday" or "delivery"

    Returns:
        Recommendation string: Yes/No with reasoning.
    """
    # 1. Get stock data
    ticker = yf.Ticker(symbol)
    period = "5d" if trade_type == "delivery" else "1d"
    data = ticker.history(period=period, interval="1h" if trade_type=="intraday" else "1d")
    
    price_trend = data['Close'].tolist()
    
    # 2. Fetch company news
    articles = fetch_latest_news(f"{symbol} stock")
    news_texts = [a["title"] for a in articles] if articles else []
    
    # 3. Build prompt
    prompt = f"""
    You are a stock analyst. Based on the following data, should a trader BUY this stock for {trade_type.upper()} trading today?

    Stock Symbol: {symbol}
    Recent Price Trend: {price_trend}
    Recent News Headlines: {news_texts}

    Respond with a clear YES or NO, followed by a short reasoning.
    """
    
    # 4. Call Gemini
    response = gemini_llm_call(prompt)
    return response


@mcp.tool()
def intraday_recommendation(action: str = "buy") -> str:
    """
    Recommend stocks to buy or sell for intraday trading based on last 24h news.

    Parameters:
        action: "buy" or "sell"

    Returns:
        A recommendation string with stock suggestions.
    """
    # 1. Fetch latest finance news
    articles = fetch_latest_news("Indian stock market")
    
    if not articles:
        return "No recent news found to analyze."
    
    # 2. Send to LLM for analysis
    news_texts = [a["title"] for a in articles]
    prompt = f"""
    Analyze the following news headlines and suggest 3 companies' stocks for intraday {action.upper()} today.
    Consider only short-term intraday movement.
    Headlines: {news_texts}
    Return a simple list of stock symbols with reasons.
    """
    
    response = gemini_llm_call(prompt)
    
    return response


if __name__ == "__main__":
    mcp.run()