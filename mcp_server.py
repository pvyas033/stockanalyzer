from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("Stock Server")


def get_stock_price_internal(symbol: str) -> dict:
    """
    Internal helper to fetch stock price using yfinance.
    Returns a dict with 'price' and 'message'.
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d")

        if not data.empty:
            price = data['Close'].iloc[-1]
            return {
                "price": float(price),
                "message": f"The current price of {symbol} is: {price:.2f}"
            }
        else:
            info = ticker.info
            price = info.get("regularMarketPrice")
            if price is not None:
                return {
                    "price": float(price),
                    "message": f"The current price of {symbol} is: {price:.2f}"
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
    """
    Compare the current stock prices of two ticker symbols.

    Parameters:
        symbol1: stock ticker symbol
        symbol2: stock ticker symbol

    Returns:
        String with the comparison of two stock prices.
    """
    result1 = get_stock_price_internal(symbol1)
    result2 = get_stock_price_internal(symbol2)

    price1 = result1.get("price")
    price2 = result2.get("price")

    # Error handling if data not available
    if price1 is None or price2 is None:
        return f"Could not get stock price for {symbol1} or {symbol2}.\n{result1['message']}\n{result2['message']}"

    # Comparison logic
    if price1 > price2:
        return f"{symbol1} (${price1:.2f}) is higher than {symbol2} (${price2:.2f})"
    elif price1 < price2:
        return f"{symbol2} (${price2:.2f}) is higher than {symbol1} (${price1:.2f})"
    else:
        return f"Both {symbol1} and {symbol2} have the same price (${price1:.2f})"


if __name__ == "__main__":
    mcp.run()