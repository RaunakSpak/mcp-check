# MCP Server Startup Script for PowerShell
Write-Host "Starting Enecovery MCP Server..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Cyan
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if fastmcp is installed
try {
    python -c "import fastmcp" 2>&1 | Out-Null
    Write-Host "FastMCP is installed" -ForegroundColor Cyan
} catch {
    Write-Host "FastMCP not found. Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Change to script directory
Set-Location $PSScriptRoot

# Run the MCP server
Write-Host ""
Write-Host "Running MCP Server..." -ForegroundColor Green
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python mcp_server.py

Read-Host "Press Enter to exit"
