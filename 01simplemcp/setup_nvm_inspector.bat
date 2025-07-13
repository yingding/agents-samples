@echo off
REM MCP Inspector Setup for NVM Windows
REM Helper script to set up MCP Inspector with NVM on Windows

echo 🔧 MCP Inspector Setup for NVM Windows
echo =========================================

echo.
echo 1. Checking NVM and Node.js status...

REM Check if NVM is available
nvm version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ NVM not found. Please install NVM for Windows first.
    echo    Download from: https://github.com/coreybutler/nvm-windows
    pause
    exit /b 1
)

echo ✅ NVM is available
nvm list

echo.
echo 2. Ensuring Node.js 22.17.0 is active...
nvm use 22.17.0

REM Verify Node.js is available
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js not available. Installing Node.js 22.17.0...
    nvm install 22.17.0
    nvm use 22.17.0
)

echo ✅ Node.js version:
node --version

echo ✅ npm version:
npm --version

echo.
echo 3. Installing MCP Inspector globally...
npm install -g @modelcontextprotocol/inspector

echo.
echo 4. Verifying MCP Inspector installation...
npx @modelcontextprotocol/inspector --version
if %errorlevel% neq 0 (
    echo ❌ MCP Inspector installation failed
    echo 💡 Try running this script as Administrator
    pause
    exit /b 1
)

echo ✅ MCP Inspector installed successfully!

echo.
echo 5. Testing MCP Inspector with your server...
echo 📤 Starting MCP Inspector...
echo 🌐 Inspector should open at: http://localhost:3000
echo ⏹️  Press Ctrl+C to stop the inspector
echo.

REM Change to the correct directory
cd /d "%~dp0"

REM Start MCP Inspector with the server
npx @modelcontextprotocol/inspector C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe mcp_server.py

echo.
echo 🛑 MCP Inspector stopped
pause
