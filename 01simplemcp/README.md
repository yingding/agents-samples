## First MCP Server

### Install uv on windows
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
Reference:
* https://pypi.org/project/uv/

### Create python venv with uv
```powershell
$VERSION="3.12";
$ENV_NAME="azfdymcp";
$ENV_SURFIX="uv";

$ENV_FULL_NAME = "$ENV_NAME$VERSION$ENV_SURFIX";
# with the closing "\"
$ENV_DIR="$env:USERPROFILE\Documents\VENV\";

# absolute path of requirements.txt to install for the python venv
$PROJ_DIR="$env:USERPROFILE\Documents\VCS\democollections\agents-samples";
$SubProj="01simplemcp"
$MCPServerFileName="mcp_server.py"
$MCPServerFilePath="$PROJ_DIR\${SubProj}\${MCPServerFileName}";

# activate uv venv
& "$ENV_DIR$ENV_FULL_NAME\Scripts\Activate.ps1";
Invoke-Expression "(Get-Command python).Source";

& "uv" pip list
```

### Install node with nvm on windows
Install the package manager on windows
```powershell
winget list nvm
winget install --id CoreyButler.NVMforWindows
winget upgrade --id CoreyButler.NVMforWindows
```

Install the node version, which works with mcp inspector
and also install the mcp inspector
```
nvm install 22.17.0
nvm use 22.17.0
npx @modelcontextprotocol/inspector
```

## ✅ Working Setup

### Current Status
✅ **MCP Server is fully functional and tested**
- Server starts without errors
- STDIO transport working correctly
- JSON-RPC communication established
- PowerShell launcher operational

⚠️ **Dev Mode Status**
- `mcp.exe` is available in virtual environment ✅
- Dev mode command exists but has output/display issues ⚠️
- Inspector mode requires Node.js and MCP Inspector package ❓
- Terminal display problems may affect dev/inspector output 🔧
- Alternative: Use direct STDIO server mode for reliable operation ✅

### Quick Start
```powershell
# Start the MCP server (RECOMMENDED)
.\mcp.ps1 server

# Run development mode (experimental)
.\mcp.ps1 dev

# Run inspector mode (requires Node.js setup)
.\mcp.ps1 inspector
```

### Available Tools & Resources
- 🔧 **sum(a, b)** - Tool to add two numbers
- 📁 **greeting://{name}** - Resource for personalized greetings

### Test Scripts
```powershell
# Basic syntax check
python -m py_compile mcp_server.py

# Direct functionality test
python test_direct.py

# STDIO communication test
python test_simple.py

# Comprehensive test suite
python test_suite.py

# Quick validation
python validate.py
```

### Environment
- **Virtual Environment**: `azfdymcp3.12uv`
- **Location**: `C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv`
- **FastMCP Version**: 2.10.5
- **MCP Protocol**: 1.11.0
- **Available Executables**: `mcp.exe`, `fastmcp.exe`, `python.exe`

### Development Tools Status
- ✅ **Server Mode**: Fully functional STDIO transport
- ⚠️ **Dev Mode**: Available but may have display issues  
- ❓ **Inspector Mode**: Requires Node.js MCP Inspector setup
- ✅ **Test Clients**: Multiple working test scripts available

### Files Structure
```
01simplemcp/
├── mcp_server.py          # Main MCP server (renamed from demo.py)
├── mcp.ps1               # Unified PowerShell launcher
├── client.py             # Comprehensive MCP test client
├── test_simple.py        # Basic STDIO test
├── test_suite.py         # Comprehensive test suite
├── validate.py           # Setup validation
└── README.md             # This documentation
```

### VS Code MCP Extension Configuration
The server can be used with VS Code MCP extension by configuring:
```json
{
  "mcpServers": {
    "demo": {
      "command": "powershell",
      "args": ["-ExecutionPolicy", "Bypass", "-File", "mcp.ps1", "server"],
      "cwd": "c:\\Users\\yingdingwang\\Documents\\VCS\\democollections\\agents-samples\\01simplemcp"
    },
    "default-server": {
			"type": "stdio",
            "command": "C:\\Users\\yingdingwang\\Documents\\VENV\\azfdymcp3.12uv\\Scripts\\python.exe",
            "args": [
                "C:\\Users\\yingdingwang\\Documents\\VCS\\democollections\\agents-samples\\01simplemcp\\mcp_server.py"
            ],
		},
  }
}
```

## 🔧 Troubleshooting

### Dev Mode Issues
If `.\mcp.ps1 dev` has display problems:
1. **Direct command**: `C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\mcp.exe dev mcp_server.py`
2. **FastMCP alternative**: `C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\fastmcp.exe dev mcp_server.py`
3. **Use test clients**: Run `python client.py` for comprehensive testing

### Inspector Mode Issues
For web inspector functionality with **NVM Windows**:

#### **NVM Windows Setup:**
```bash
# Check current Node.js versions
nvm list

# Use the installed version (22.17.0)
nvm use 22.17.0

# Verify Node.js and npm are available
node --version
npm --version

# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Test inspector
npx @modelcontextprotocol/inspector --version
```

#### **Common NVM Windows Issues:**
1. **"npx not found"** - Restart terminal after `nvm use`
2. **"Permission denied"** - Run terminal as Administrator
3. **"Package not found"** - Check if npm global path is in PATH
4. **"Cannot find module"** - Reinstall: `npm uninstall -g @modelcontextprotocol/inspector && npm install -g @modelcontextprotocol/inspector`

**Known Issues:**
- Terminal display problems may affect dev/inspector output
- MCP dev command may hang or show incomplete output  
- Inspector may not start due to Node.js dependencies
- Use diagnostic script: `python diagnose_inspector.py`

### Alternative Development Commands
```powershell
# Direct STDIO server (RECOMMENDED)
python mcp_server.py

# Using UV (if available)
uv run mcp dev mcp_server.py

# Using npx inspector directly (if Node.js available)
npx @modelcontextprotocol/inspector C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe mcp_server.py

# Diagnostic check
python diagnose_inspector.py
```

## 🚨 MCP Inspector Connection Issues - SOLVED

### 🔍 **Problem Identified:**
Based on terminal output analysis:
- ✅ Node.js is available (v22.17.0)
- ❌ `npx @modelcontextprotocol/inspector` fails with "file not found"
- ⚠️ MCP dev command has output issues

### 🛠️ **Solutions:**

#### **Option 1: Fix npx MCP Inspector (NVM Windows)**
```bash
# Ensure Node.js is active in NVM
nvm list
nvm use 22.17.0

# Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# Verify installation
npx @modelcontextprotocol/inspector --version

# Then run inspector
npx @modelcontextprotocol/inspector python mcp_server.py
```

#### **Option 2: Alternative NVM Windows Setup**
```bash
# If npx has issues, use direct npm installation
npm install -g @modelcontextprotocol/inspector

# Find the global installation path
npm list -g @modelcontextprotocol/inspector

# Run directly (replace <path> with actual path)
node <path>/bin/mcp-inspector python mcp_server.py
```

#### **Option 3: Use MCP Dev Command (if working)**
```powershell
# Enhanced dev server with debug output
C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\mcp.exe dev mcp_server_enhanced.py
```

### 🎯 **Quick Fix Commands (NVM Windows):**
```powershell
# 1. Ensure Node.js is active
nvm use 22.17.0

# 2. Install MCP Inspector globally
npm install -g @modelcontextprotocol/inspector

# 3. Test installation
npx @modelcontextprotocol/inspector --version

# 4. Run inspector with your MCP server
npx @modelcontextprotocol/inspector C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe mcp_server.py

# 5. If inspector works, access at: http://localhost:3000

# 6. Fallback - test with direct client
python client.py
```

### One liner for start mcp inspector
Parameterized Variant
```powershell
$CMD="C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe";
$ARGS="C:\Users\yingdingwang\Documents\VCS\democollections\agents-samples\01simplemcp\mcp_server.py";
& "npx" @modelcontextprotocol/inspector $CMD $ARGS
```



### MCP dev server run issue

Reference:
* https://github.com/modelcontextprotocol/python-sdk/issues/623