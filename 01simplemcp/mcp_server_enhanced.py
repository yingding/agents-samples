# MCP Server with Inspector Support
# Enhanced version that works better with MCP Inspector

from mcp.server.fastmcp import FastMCP
import sys
import asyncio

# Create MCP server with explicit configuration
mcp = FastMCP("Demo", version="1.0.0")

@mcp.tool()
def sum(a: int, b: int) -> int:
    """Add two numbers together"""
    result = a + b
    print(f"[DEBUG] sum({a}, {b}) = {result}", file=sys.stderr)
    return result

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting for the given name"""
    greeting = f"Hello, {name}! Welcome to the MCP Demo Server."
    print(f"[DEBUG] Generated greeting for: {name}", file=sys.stderr)
    return greeting

def main():
    """Main entry point for the MCP server"""
    try:
        print("[DEBUG] Starting MCP Demo Server...", file=sys.stderr)
        print("[DEBUG] Available tools: sum", file=sys.stderr)
        print("[DEBUG] Available resources: greeting://{name}", file=sys.stderr)
        print("[DEBUG] Server ready for connections", file=sys.stderr)
        
        # Run with STDIO transport (works with both direct and inspector)
        mcp.run(transport='stdio')
        
    except KeyboardInterrupt:
        print("[DEBUG] Server stopped by user", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"[ERROR] Server error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
