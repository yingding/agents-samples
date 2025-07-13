# MCP Server Launcher - FastMCP Server
# Usage: .\mcp.ps1 [server|dev|inspector]
param([string]$Mode = "help")

$venv = "$env:USERPROFILE\Documents\VENV\azfdymcp3.12uv"
$python = "$venv\Scripts\python.exe"
$mcp = "$venv\Scripts\mcp.exe"
$demo = Join-Path $PSScriptRoot "mcp_server.py"

# Validate prerequisites
if (!(Test-Path $python)) { Write-Host "❌ Python not found: $python" -ForegroundColor Red; exit 1 }
if (!(Test-Path $demo)) { Write-Host "❌ MCP server script not found: $demo" -ForegroundColor Red; exit 1 }

switch ($Mode.ToLower()) {
    "server" {
        Write-Host "� Starting MCP Server..." -ForegroundColor Green
        & $python $demo
    }
    "dev" {
        if (!(Test-Path $mcp)) { Write-Host "❌ MCP not found: $mcp" -ForegroundColor Red; exit 1 }
        Write-Host "🔧 Starting MCP Dev Server..." -ForegroundColor Green
        & $mcp dev $demo
    }
    "inspector" {
        if (!(Test-Path $mcp)) { Write-Host "❌ MCP not found: $mcp" -ForegroundColor Red; exit 1 }
        Write-Host "🔍 Starting MCP Inspector..." -ForegroundColor Green
        Start-Job { param($url); Start-Sleep 3; Start-Process $url } -ArgumentList "http://localhost:3000" | Out-Null
        & $mcp dev $demo
    }
}
