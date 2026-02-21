# Quick Start Guide - Running MCP Server Automatically

## ✅ Server Status
- ✅ Python 3.11.0 detected
- ✅ FastMCP installed
- ✅ 58 HTML files found
- ✅ Server ready to run

## 🚀 How to Run the Server Automatically

### Method 1: Double-Click (Easiest)
1. **Double-click** `run_mcp_server.bat`
2. The server will start automatically
3. A window will show server status

### Method 2: PowerShell
1. Right-click `run_mcp_server.ps1`
2. Select "Run with PowerShell"
3. Or open PowerShell and run:
   ```powershell
   .\run_mcp_server.ps1
   ```

### Method 3: Command Prompt
1. Open Command Prompt
2. Navigate to the project folder
3. Run:
   ```cmd
   run_mcp_server.bat
   ```

### Method 4: Direct Python
```bash
python mcp_server.py
```

## 📋 What the Scripts Do

The startup scripts automatically:
1. ✅ Check if Python is installed
2. ✅ Check if FastMCP is installed
3. ✅ Install dependencies if needed
4. ✅ Start the MCP server
5. ✅ Show server status and available tools

## 🔧 Server Information

When the server starts, you'll see:
```
============================================================
Enecovery Website MCP Server
============================================================
Base directory: D:\Raunak 2025\Enecovery-new - Copy
HTML files found: 58
============================================================
Server starting...
Available tools:
  - read_page
  - extract_text
  - get_metadata
  - list_pages
  - search_content
  - get_sitemap
============================================================
Waiting for MCP client connections...
Press Ctrl+C to stop the server
============================================================
```

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal window to stop the server.

## 📝 Next Steps

1. **Configure MCP Client**: Add the server to your MCP client configuration
2. **Test Tools**: Use the available tools to interact with your website
3. **Integrate**: Connect the server to your AI assistant (Claude Desktop, Cursor, etc.)

## ⚙️ MCP Client Configuration

Add this to your MCP client config (e.g., `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "enecovery-website": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "D:\\Raunak 2025\\Enecovery-new - Copy"
    }
  }
}
```

**Note**: Update the `cwd` path to match your actual directory.

## 🆘 Troubleshooting

- **Python not found**: Install Python 3.8+ from python.org
- **FastMCP error**: Run `pip install fastmcp`
- **File not found**: Make sure you're in the correct directory
- **Permission error**: Run as administrator if needed
