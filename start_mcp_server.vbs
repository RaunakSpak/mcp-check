' VBScript to run MCP server in a hidden window (for background execution)
Set WshShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Change to script directory
WshShell.CurrentDirectory = scriptDir

' Run the MCP server (0 = hidden window, 1 = normal window)
WshShell.Run "python mcp_server.py", 1, False

' Optional: Uncomment the line below to run in background (hidden)
' WshShell.Run "python mcp_server.py", 0, False
