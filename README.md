# Stock Analyzer MCP Server

A Model Context Protocol (MCP) server that provides real-time stock price analysis tools for Claude Desktop. This server offers two powerful tools to analyze stock market data using the Yahoo Finance API.

## 🚀 Features

- **Real-time Stock Prices**: Get current stock prices for any ticker symbol
- **Stock Comparison**: Compare prices between two different stocks
- **Easy Integration**: Seamlessly integrates with Claude Desktop
- **Reliable Data**: Uses Yahoo Finance API for accurate market data

## 📋 Available Tools

### 1. `get_stock_price`
Get the current stock price for any ticker symbol.

**Parameters:**
- `symbol` (string): Stock ticker symbol (e.g., "AAPL", "MSFT", "GOOGL")

**Example Usage:**
- "What is the current price of Apple stock?"
- "Get me the price of TSLA"

### 2. `compare_stocks`
Compare the current stock prices of two different ticker symbols.

**Parameters:**
- `symbol1` (string): First stock ticker symbol
- `symbol2` (string): Second stock ticker symbol

**Example Usage:**
- "Compare Apple and Microsoft stock prices"
- "Which is higher: Tesla or Ford?"

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Claude Desktop application
- Internet connection for stock data

### Step 1: Download Claude Desktop

1. Visit the official Claude website: [https://claude.ai/](https://claude.ai/)
2. Click on "Download Claude Desktop" or navigate to the downloads section
3. Download the appropriate version for your operating system:
   - **macOS**: Download the `.dmg` file
   - **Windows**: Download the `.exe` installer
   - **Linux**: Download the `.AppImage` or `.deb` package

### Step 2: Install Claude Desktop

#### macOS Installation:
1. Open the downloaded `.dmg` file
2. Drag Claude Desktop to your Applications folder
3. Launch Claude Desktop from Applications

#### Windows Installation:
1. Run the downloaded `.exe` installer
2. Follow the installation wizard
3. Launch Claude Desktop from Start menu

#### Linux Installation:
1. Make the `.AppImage` executable: `chmod +x Claude-Desktop-*.AppImage`
2. Run: `./Claude-Desktop-*.AppImage`
3. Or install the `.deb` package: `sudo dpkg -i claude-desktop-*.deb`

### Step 3: Set Up the MCP Server

1. **Clone or Download this Repository:**
   ```bash
   git clone <repository-url>
   cd stockanalyzer
   ```

2. **Create Virtual Environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment:**
   ```bash
   # macOS/Linux
   source venv/bin/activate
   
   # Windows
   venv\Scripts\activate
   ```

4. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Test the Server:**
   ```bash
   python mcp_client.py
   ```
   Try asking: "What is the price of AAPL?"

### Step 4: Configure Claude Desktop

1. **Locate Claude Desktop Configuration File:**
   
   **macOS:**
   ```
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```
   
   **Windows:**
   ```
   %APPDATA%\Claude\claude_desktop_config.json
   ```
   
   **Linux:**
   ```
   ~/.config/Claude/claude_desktop_config.json
   ```

2. **Create or Edit the Configuration File:**
   
   If the file doesn't exist, create it. If it exists, add the MCP server configuration to the existing `mcpServers` section.

3. **Add MCP Server Configuration:**
   
   Use the sample configuration from `claude_desktop_config.sample.json` and replace the placeholders:

   ```json
   {
     "mcpServers": {
       "stock-analyzer": {
         "command": "/absolute/path/to/your/venv/bin/python",
         "args": ["/absolute/path/to/your/mcp_server.py"]
       }
     }
   }
   ```

   **Example for macOS:**
   ```json
   {
     "mcpServers": {
       "stock-analyzer": {
         "command": "/Users/username/Projects/stockanalyzer/venv/bin/python",
         "args": ["/Users/username/Projects/stockanalyzer/mcp_server.py"]
       }
     }
   }
   ```

   **Example for Windows:**
   ```json
   {
     "mcpServers": {
       "stock-analyzer": {
         "command": "C:\\Users\\username\\Projects\\stockanalyzer\\venv\\Scripts\\python.exe",
         "args": ["C:\\Users\\username\\Projects\\stockanalyzer\\mcp_server.py"]
       }
     }
   }
   ```

   **Example for Linux:**
   ```json
   {
     "mcpServers": {
       "stock-analyzer": {
         "command": "/home/username/Projects/stockanalyzer/venv/bin/python",
         "args": ["/home/username/Projects/stockanalyzer/mcp_server.py"]
       }
     }
   }
   ```

### Step 5: Restart Claude Desktop

1. **Completely quit Claude Desktop:**
   - Close all Claude Desktop windows
   - On macOS: Right-click Claude Desktop in Dock → Quit
   - On Windows: Close from system tray or Task Manager
   - On Linux: Kill the process or close all windows

2. **Reopen Claude Desktop:**
   - Launch Claude Desktop from Applications/Start menu
   - Wait for it to fully load

### Step 6: Verify Integration

1. **Check MCP Server Status:**
   - In Claude Desktop, look for MCP server indicators
   - You should see "stock-analyzer" in the connected servers list

2. **Test the Tools:**
   Try these example queries in Claude Desktop:
   
   **Single Stock Price:**
   - "What is the current price of Apple stock?"
   - "Get me the price of Tesla (TSLA)"
   - "How much is Microsoft stock trading at?"
   
   **Stock Comparison:**
   - "Compare Apple and Microsoft stock prices"
   - "Which is higher: Tesla or Ford?"
   - "Compare the prices of GOOGL and META"

## 🔧 Troubleshooting

### Common Issues

#### 1. MCP Server Not Appearing
- **Check file paths**: Ensure all paths in the config are absolute and correct
- **Verify Python environment**: Make sure the virtual environment is properly set up
- **Check permissions**: Ensure the Python executable has execute permissions

#### 2. "Command not found" Error
- **Update paths**: Use absolute paths for both command and args
- **Check virtual environment**: Ensure the venv is activated and dependencies are installed

#### 3. Server Disconnects Unexpectedly
- **Check logs**: Look at Claude Desktop logs in:
  - **macOS**: `~/Library/Logs/Claude/`
  - **Windows**: `%APPDATA%\Claude\logs\`
  - **Linux**: `~/.config/Claude/logs/`

#### 4. Stock Data Not Loading
- **Check internet connection**: Ensure you have internet access
- **Verify ticker symbols**: Use correct stock ticker symbols (e.g., "AAPL" not "Apple")
- **Test manually**: Run `python mcp_client.py` to test the server independently

### Debugging Steps

1. **Test Server Manually:**
   ```bash
   cd /path/to/stockanalyzer
   source venv/bin/activate
   python mcp_client.py
   ```

2. **Check Claude Desktop Logs:**
   Look for files like:
   - `mcp-server-stock-analyzer.log`
   - `mcp.log`
   - `main.log`

3. **Verify Configuration:**
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   type %APPDATA%\Claude\claude_desktop_config.json
   
   # Linux
   cat ~/.config/Claude/claude_desktop_config.json
   ```

## 📁 Project Structure

```
stockanalyzer/
├── mcp_server.py              # Main MCP server implementation
├── mcp_client.py              # Test client for development
├── requirements.txt           # Python dependencies
├── claude_desktop_config.json # Working Claude Desktop config
├── claude_desktop_config.sample.json # Sample config template
├── README.md                  # This file
└── venv/                     # Python virtual environment
```

## 🧪 Development & Testing

### Running Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Test the server
python mcp_client.py

# Test specific functionality
echo "What is the price of AAPL?" | python mcp_client.py
```

### Adding New Tools
1. Add new functions to `mcp_server.py`
2. Decorate with `@mcp.tool()`
3. Update documentation
4. Test with `mcp_client.py`

## 📝 Dependencies

- `mcp>=1.14.1` - Model Context Protocol SDK
- `yfinance>=0.2.65` - Yahoo Finance API client
- `google-generativeai>=0.8.5` - Google AI integration
- `python-dotenv>=1.0.1` - Environment variable management
- `pandas>=1.5.0` - Data manipulation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

If you encounter any issues:

1. Check the troubleshooting section above
2. Review Claude Desktop logs
3. Test the server independently
4. Create an issue with detailed error information

## 🎯 Quick Start Summary

1. **Download** Claude Desktop from [claude.ai](https://claude.ai/)
2. **Install** Claude Desktop
3. **Set up** the MCP server (clone repo, create venv, install deps)
4. **Configure** Claude Desktop with the MCP server paths
5. **Restart** Claude Desktop
6. **Test** by asking: "What is the price of AAPL?"

Enjoy analyzing stocks with Claude Desktop! 🚀📈