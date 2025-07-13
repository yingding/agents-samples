# Direct MCP Server Test
# Test the MCP server functionality directly

import sys
import os

def test_direct():
    """Test MCP server imports and basic functionality"""
    print("🔬 Direct MCP Server Test")
    print("=" * 30)
    
    try:
        # Test if we can import the MCP server
        print("1. Testing mcp_server.py import...")
        
        # Add current directory to path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Try to import mcp_server
        import mcp_server
        print("   ✅ mcp_server.py imports successfully")
        
        # Check if FastMCP is available
        print("2. Testing FastMCP availability...")
        try:
            from mcp.server.fastmcp import FastMCP
            print("   ✅ FastMCP is available")
        except ImportError as e:
            print(f"   ❌ FastMCP import failed: {e}")
            return
        
        # Test if we can access the server tools
        print("3. Testing server configuration...")
        if hasattr(mcp_server, 'mcp'):
            print("   ✅ MCP server instance found")
            
            # Try to get tools information
            tools = getattr(mcp_server.mcp, '_tools', {})
            if tools:
                print(f"   ✅ Found {len(tools)} tool(s):")
                for tool_name in tools.keys():
                    print(f"      🔧 {tool_name}")
            else:
                print("   ⚠️  No tools found")
                
            # Try to get resources information  
            resources = getattr(mcp_server.mcp, '_resources', {})
            if resources:
                print(f"   ✅ Found {len(resources)} resource(s):")
                for resource_name in resources.keys():
                    print(f"      📁 {resource_name}")
            else:
                print("   ⚠️  No resources found")
        else:
            print("   ❌ MCP server instance not found")
            
        print("\n4. Testing sum function directly...")
        if hasattr(mcp_server, 'sum'):
            result = mcp_server.sum(5, 3)
            print(f"   ✅ sum(5, 3) = {result}")
        else:
            print("   ❌ sum function not found")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n{'='*30}")
    print("🎯 Test Summary:")
    print("   If all tests pass, your MCP server is ready!")
    print("   You can now run: ./mcp.ps1 server")

if __name__ == "__main__":
    test_direct()
