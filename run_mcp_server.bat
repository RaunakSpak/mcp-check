@echo off
REM MCP Server Startup Script for Windows
echo Starting Enecovery MCP Server...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if fastmcp is installed
python -c "import fastmcp" >nul 2>&1
if errorlevel 1 (
    echo FastMCP not found. Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Change to script directory
cd /d "%~dp0"

REM Run the MCP server
echo Running MCP Server...
echo Press Ctrl+C to stop the server
echo.
python mcp_server.py

pause
