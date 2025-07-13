## SQL MCP

## FastMCP 2.0
* https://gofastmcp.com/getting-started/welcome

## Testing

### One liner for start mcp inspector
Parameterized Variant
```powershell
$CMD="C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe";
$SUB_PROJ="02sqlmcp";
$MCP_ARGS="C:\Users\yingdingwang\Documents\VCS\democollections\agents-samples\${SUB_PROJ}\mcp_server.py";
Write-Host "ARGS value: ${MCP_ARGS}"
& "npx" @modelcontextprotocol/inspector $CMD ${MCP_ARGS}
```

