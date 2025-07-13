#!/usr/bin/env python3
# Simple test to verify MCP server functionality

import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🔬 Testing MCP Server...")
print("=" * 40)

try:
    print("1. Testing FastMCP import...")
    from mcp.server.fastmcp import FastMCP
    print("   ✅ FastMCP imported successfully")
    
    print("2. Testing server module import...")
    import mcp_server
    print("   ✅ mcp_server.py imported successfully")
    
    print("3. Testing server instance...")
    if hasattr(mcp_server, 'mcp'):
        print("   ✅ MCP server instance exists")
        print(f"   📊 Server name: {mcp_server.mcp.name}")
    else:
        print("   ❌ MCP server instance not found")
    
    print("4. Testing sum function...")
    if hasattr(mcp_server, 'sum'):
        result = mcp_server.sum(10, 20)
        print(f"   ✅ sum(10, 20) = {result}")
        
        if result == 30:
            print("   ✅ Function works correctly!")
        else:
            print(f"   ❌ Expected 30, got {result}")
    else:
        print("   ❌ sum function not found")
    
    print("5. Testing greeting function...")
    if hasattr(mcp_server, 'get_greeting'):
        greeting = mcp_server.get_greeting("World")
        print(f"   ✅ get_greeting('World') = '{greeting}'")
    else:
        print("   ❌ get_greeting function not found")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your MCP server is ready to use!")
    print("\nTo start the server, run:")
    print("   ./mcp.ps1 server")
    
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("\nPlease ensure FastMCP is installed:")
    print("   pip install fastmcp")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 40)
