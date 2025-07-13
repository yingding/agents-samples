## SQL MCP

## FastMCP 2.0
* https://gofastmcp.com/getting-started/welcome

## Testing

### One liner for start mcp inspector
```powershell
$VERSION="3.12";
$ENV_NAME="azfdymcp";
$ENV_SURFIX="uv";

$ENV_FULL_NAME = "$ENV_NAME$VERSION$ENV_SURFIX";
# with the closing "\"
$ENV_DIR="$env:USERPROFILE\Documents\VENV\";

# absolute path of requirements.txt to install for the python venv
$PROJ_DIR="$env:USERPROFILE\Documents\VCS\democollections\agents-samples";
$SubProj="02sqlmcp"
$MCPServerFileName="mcp_server.py"
$MCPServerFilePath="$PROJ_DIR\${SubProj}\${MCPServerFileName}";

# activate uv venv
& "$ENV_DIR$ENV_FULL_NAME\Scripts\Activate.ps1";
Invoke-Expression "(Get-Command python).Source";

& "uv" pip list
```


Parameterized Variant
```powershell
$CMD="C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe";
$SUB_PROJ="02sqlmcp";
$MCP_ARGS="`"C:\Users\yingdingwang\Documents\VCS\democollections\agents-samples\${SUB_PROJ}\mcp_server.py`"";
Write-Host "Arguments: ${MCP_ARGS}"
& "npx" @modelcontextprotocol/inspector $CMD ${MCP_ARGS}
```

```test

```