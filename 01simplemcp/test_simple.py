# Simple MCP Test Client
# Quick test of MCP server basic functionality

import json
import subprocess
import sys
import time

def test_simple():
    """Simple test of MCP server"""
    print("🧪 Simple MCP Server Test")
    print("=" * 30)
    
    # Start server
    cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "mcp.ps1", "server"]
    
    try:
        process = subprocess.Popen(
            cmd, 
            stdin=subprocess.PIPE, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Server started")
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "simple-test", "version": "1.0.0"}
            }
        }
        
        print("📤 Sending initialize request...")
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()
        
        # Read response
        response = process.stdout.readline()
        if response:
            print(f"📥 Response received: {len(response)} chars")
            try:
                data = json.loads(response.strip())
                if "result" in data:
                    print("✅ Server initialized successfully")
                    print(f"   Server: {data['result'].get('serverInfo', {}).get('name', 'Unknown')}")
                    print(f"   Version: {data['result'].get('serverInfo', {}).get('version', 'Unknown')}")
                else:
                    print(f"❌ Error: {data.get('error', 'Unknown error')}")
            except json.JSONDecodeError:
                print(f"❌ Invalid JSON: {response[:100]}...")
        else:
            print("❌ No response received")
            
        # Check for errors
        if process.poll() is not None:
            stderr = process.stderr.read()
            if stderr:
                print(f"❌ Server error: {stderr}")
        
        process.terminate()
        process.wait()
        print("🛑 Server stopped")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_simple()
