# Quick MCP STDIO Test
# Simple validation that MCP server is working via STDIO

import subprocess
import json
import sys

def quick_test():
    print("🔬 Quick MCP STDIO Test")
    print("-" * 25)
    
    # Test server startup
    try:
        print("1. Testing server startup...")
        result = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", 
             "& './mcp.ps1' server | Select-Object -First 1"],
            capture_output=True, text=True, timeout=5
        )
        
        if result.returncode == 0:
            print("   ✅ Server can start")
        else:
            print(f"   ❌ Server failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("   ✅ Server started (timeout as expected for STDIO)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test MCP tools availability
    print("\n2. Testing MCP availability...")
    try:
        result = subprocess.run(
            ["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command",
             "Test-Path 'C:/Users/yingdingwang/Documents/VENV/azfdymcp3.12uv/Scripts/mcp.exe'"],
            capture_output=True, text=True
        )
        
        if "True" in result.stdout:
            print("   ✅ MCP executable found")
        else:
            print("   ❌ MCP executable not found")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test mcp_server.py syntax
    print("\n3. Testing mcp_server.py syntax...")
    try:
        result = subprocess.run([
            "C:/Users/yingdingwang/Documents/VENV/azfdymcp3.12uv/Scripts/python.exe",
            "-m", "py_compile", "mcp_server.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ mcp_server.py syntax is valid")
        else:
            print(f"   ❌ mcp_server.py syntax error: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print(f"\n{'='*25}")
    print("🎯 Manual Test Instructions:")
    print("1. Run: ./mcp.ps1 server")
    print("2. In another terminal, connect with MCP client")
    print("3. Or use VS Code MCP extension with 'server' config")
    print("\n📋 Available for testing:")
    print("   🔧 sum(a, b) - Add two numbers")
    print("   📁 greeting://{name} - Get personalized greeting")

if __name__ == "__main__":
    quick_test()
