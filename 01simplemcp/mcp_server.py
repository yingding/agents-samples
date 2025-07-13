# FastMCP Demo Server
# Simple MCP server with basic tools and resources
from mcp.server.fastmcp import FastMCP
import sys

# Create MCP server
mcp = FastMCP("Demo")

# tools
@mcp.tool()
def sum(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# resources
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    try:
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)