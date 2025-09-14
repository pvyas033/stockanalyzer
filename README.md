# 📈 Stock Analyzer with MCP + Gemini + yFinance

This project demonstrates how to build an **AI-powered stock price analyzer** using:
- [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol)  
- [Google Gemini](https://ai.google.dev/) for natural language understanding  
- [yFinance](https://github.com/ranaroussi/yfinance) for real-time stock data  

---

## ⚙️ Installation

1. **Clone this repository**
   ```bash
   git clone https://github.com/yourusername/stockanalyzer.git
   cd stockanalyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Mac/Linux:**
     ```bash
     source venv/bin/activate
     ```
   - **Windows (PowerShell):**
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```bash
     venv\Scripts\activate.bat
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up API key**  
   Create a `.env` file in the root folder:
   ```ini
   GOOGLE_API_KEY=your_google_api_key_here
   ```

---

## 🚀 Usage

Run the client:
```bash
python client.py
```

### Example interactions

#### Get stock price
```
What is your query? : What is the stock price of walmart?
--------------------------------------------------
The user input is :  What is the stock price of walmart?
Connection established, creation session started.
[agent] Session created, initializing MCP server...
[agent] MCP server initialized.
Processing request of type ListToolsRequest
To execute  the User Query: What is the stock price of walmart? - The Identified tool is get_stock_price, and the parameters required are {'symbol': 'WMT'}
Processing request of type CallToolRequest
The current price of WMT is: 103.49
--------------------------------------------------
```

#### Compare two stocks
```
What is your query? : Could you please compare walmart and apple stock price?
--------------------------------------------------
The user input is :  Could you please compare walmart and apple stock price?
Connection established, creation session started.
[agent] Session created, initializing MCP server...
[agent] MCP server initialized.
Processing request of type ListToolsRequest
To execute  the User Query: Could you please compare walmart and apple stock price? - The Identified tool is compare_stocks, and the parameters required are {'symbol1': 'WMT', 'symbol2': 'AAPL'}
Processing request of type CallToolRequest
AAPL ($234.07) is higher than WMT ($103.49)
--------------------------------------------------
```

---

## 📂 Project Structure
```
stockanalyzer/
│── mcp_Server.py        # MCP server exposing stock tools
│── client.py            # MCP client powered by Gemini
│── requirements.txt     # Dependencies
│── .env.example         # Example environment variables
│── .gitignore           # Git ignore rules
│── README.md            # Documentation
```

---

## 🛠️ Tools Implemented

1. **get_stock_price** → Fetch latest stock price of a company.  
2. **compare_stocks** → Compare two stock prices.  

---

## Demo

Check out full demo how this works:
[Agent Stock Analyzer](https://pankajvyas.in/demo/stockana.mp4)
