# MCP Server for Enecovery Website

This MCP (Model Context Protocol) server provides tools to interact with the Enecovery static HTML website. It allows AI assistants to read, search, and extract information from HTML pages.

## Features

The MCP server provides the following tools:

1. **read_page** - Read the full content of an HTML page
2. **extract_text** - Extract plain text from HTML (removes all tags)
3. **get_metadata** - Extract metadata (title, description, keywords, headings, links)
4. **list_pages** - List all available HTML pages
5. **search_content** - Search for text across HTML files
6. **get_sitemap** - Get sitemap information with priorities

## Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

Or install FastMCP directly:
```bash
pip install fastmcp
```

2. The MCP server is ready to use!

## Usage

### With Cursor/Claude Desktop

Add the following configuration to your MCP settings (usually in `~/.cursor/mcp.json` or similar):

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

**Note:** Update the `cwd` path to match your actual project directory.

### Running the Server

#### Option 1: Double-click the batch file (Windows)
Simply double-click `run_mcp_server.bat` to start the server.

#### Option 2: Run from PowerShell
```powershell
.\run_mcp_server.ps1
```

#### Option 3: Run from Command Prompt
```cmd
run_mcp_server.bat
```

#### Option 4: Run directly with Python
```bash
python mcp_server.py
```

The server communicates via stdio using the MCP protocol and will display startup information when launched.

## Tool Examples

### Read a Page
```json
{
  "name": "read_page",
  "arguments": {
    "filepath": "index.html"
  }
}
```

### Extract Text
```json
{
  "name": "extract_text",
  "arguments": {
    "filepath": "aboutus.html"
  }
}
```

### Get Metadata
```json
{
  "name": "get_metadata",
  "arguments": {
    "filepath": "waste-to-enegry.html"
  }
}
```

### List All Pages
```json
{
  "name": "list_pages",
  "arguments": {}
}
```

### Search Content
```json
{
  "name": "search_content",
  "arguments": {
    "query": "waste to energy",
    "filepath": null
  }
}
```

### Get Sitemap
```json
{
  "name": "get_sitemap",
  "arguments": {}
}
```

## Project Structure

```
.
├── mcp_server.py      # Main MCP server implementation
├── requirements.txt   # Python dependencies
├── mcp.json          # MCP configuration example
├── README_MCP.md     # This file
├── index.html        # Website HTML files
├── aboutus.html
├── sitemap.xml
└── ... (other HTML files)
```

## Notes

- The server uses **FastMCP** (recommended Python MCP framework)
- The server reads HTML files from the directory where `mcp_server.py` is located
- All file paths are relative to the base directory
- Text extraction removes script and style tags automatically
- Search is case-insensitive
- Metadata extraction includes title, description, keywords, headings (h1-h3), and links

## Troubleshooting

1. **File not found errors**: Ensure the HTML files are in the same directory as `mcp_server.py`
2. **Import errors**: Make sure you've installed all dependencies with `pip install -r requirements.txt`
3. **Encoding issues**: The server uses UTF-8 encoding for all file operations

## License

This MCP server is provided as-is for use with the Enecovery website.
