#!/usr/bin/env python3
# MCP Inspector Connection Troubleshooting
# Diagnose why MCP inspector can't connect to the server

import subprocess
import json
import time
import os
import sys

def test_mcp_inspector_connection():
    """Test MCP inspector connection issues"""
    print("🔍 MCP Inspector Connection Troubleshooting")
    print("=" * 50)
    
    # First, test if the basic server works
    print("1. Testing basic MCP server (STDIO)...")
    
    venv_python = r"C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe"
    server_script = "mcp_server.py"
    
    try:
        # Start the basic server
        process = subprocess.Popen(
            [venv_python, server_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )
        
        print("   ✅ Basic server started")
        
        # Send initialize request
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "inspector-test", "version": "1.0.0"}
            }
        }
        
        request_str = json.dumps(init_request) + '\n'
        process.stdin.write(request_str)
        process.stdin.flush()
        
        # Wait for response
        time.sleep(1)
        
        if process.poll() is None:
            print("   ✅ Server is running and accepting input")
            
            # Try to read response
            try:
                response = process.stdout.readline()
                if response:
                    print(f"   ✅ Server responded: {response[:100]}...")
                    try:
                        data = json.loads(response.strip())
                        print("   ✅ Valid JSON response received")
                    except json.JSONDecodeError:
                        print("   ⚠️  Response is not valid JSON")
                else:
                    print("   ❌ No response from server")
            except Exception as e:
                print(f"   ❌ Error reading response: {e}")
        else:
            print(f"   ❌ Server exited with code: {process.returncode}")
            stderr = process.stderr.read()
            if stderr:
                print(f"   📝 Error: {stderr}")
        
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"   ❌ Failed to test basic server: {e}")
    
    # Test MCP dev command
    print("\n2. Testing MCP dev command...")
    
    mcp_exe = r"C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\mcp.exe"
    
    if os.path.exists(mcp_exe):
        try:
            print(f"   📤 Running: {mcp_exe} dev {server_script}")
            
            # Test with short timeout to see if it starts
            process = subprocess.Popen(
                [mcp_exe, "dev", server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            
            time.sleep(3)  # Wait 3 seconds
            
            if process.poll() is None:
                print("   ✅ MCP dev server appears to be running")
                
                # Check if it's listening on a port
                try:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(('localhost', 3000))
                    if result == 0:
                        print("   ✅ Server is listening on port 3000")
                    else:
                        print("   ❌ Server not listening on port 3000")
                    sock.close()
                except Exception as e:
                    print(f"   ⚠️  Could not check port 3000: {e}")
                
                # Try to send a request to dev server
                init_request = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "initialize",
                    "params": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "clientInfo": {"name": "dev-test", "version": "1.0.0"}
                    }
                }
                
                try:
                    request_str = json.dumps(init_request) + '\n'
                    process.stdin.write(request_str)
                    process.stdin.flush()
                    
                    time.sleep(1)
                    
                    # Try to read response (non-blocking)
                    import select
                    ready, _, _ = select.select([process.stdout], [], [], 2)
                    if ready:
                        response = process.stdout.readline()
                        if response:
                            print(f"   ✅ Dev server responded: {response[:100]}...")
                        else:
                            print("   ❌ No response from dev server")
                    else:
                        print("   ⏱️  Timeout waiting for dev server response")
                        
                except Exception as e:
                    print(f"   ❌ Error communicating with dev server: {e}")
            else:
                print(f"   ❌ MCP dev server exited with code: {process.returncode}")
                stderr = process.stderr.read()
                stdout = process.stdout.read()
                if stderr:
                    print(f"   📝 STDERR: {stderr}")
                if stdout:
                    print(f"   📝 STDOUT: {stdout}")
            
            process.terminate()
            process.wait()
            
        except Exception as e:
            print(f"   ❌ Failed to test MCP dev: {e}")
    else:
        print(f"   ❌ MCP executable not found: {mcp_exe}")
    
    # Check Node.js and MCP Inspector (NVM Windows support)
    print("\n3. Checking MCP Inspector requirements (NVM Windows)...")
    
    try:
        # Check Node.js version with NVM
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            node_version = result.stdout.strip()
            print(f"   ✅ Node.js available: {node_version}")
            
            # Check npm version
            npm_result = subprocess.run(["npm", "--version"], capture_output=True, text=True, timeout=5)
            if npm_result.returncode == 0:
                print(f"   ✅ npm available: {npm_result.stdout.strip()}")
            
            # Test npx availability
            print("   📤 Testing npx availability...")
            npx_result = subprocess.run(["npx", "--version"], capture_output=True, text=True, timeout=5)
            if npx_result.returncode == 0:
                print(f"   ✅ npx available: {npx_result.stdout.strip()}")
                
                # Test MCP Inspector with npx
                print("   📤 Testing MCP Inspector availability...")
                result = subprocess.run(
                    ["npx", "--yes", "@modelcontextprotocol/inspector", "--version"],
                    capture_output=True, text=True, timeout=15
                )
                if result.returncode == 0:
                    print("   ✅ MCP Inspector available via npx")
                else:
                    print("   ❌ MCP Inspector not available via npx")
                    if result.stderr:
                        print(f"      Error: {result.stderr[:200]}...")
                    
                    # Suggest manual installation
                    print("   💡 Try manual installation:")
                    print("      npm install -g @modelcontextprotocol/inspector")
            else:
                print("   ❌ npx not available (NVM issue?)")
                print("   💡 Try: nvm use <node-version> or restart terminal")
        else:
            print("   ❌ Node.js not available")
            print("   💡 NVM Windows commands:")
            print("      nvm list")
            print("      nvm use <version>")
            
    except Exception as e:
        print(f"   ❌ Node.js/npx check failed: {e}")
        print("   💡 NVM Windows troubleshooting:")
        print("      1. Open new terminal as Administrator")
        print("      2. Run: nvm use <node-version>")
        print("      3. Verify: node --version && npm --version")
    
    print(f"\n{'='*50}")
    print("🎯 MCP Inspector Connection Summary:")
    print("   1. Basic STDIO server should work for direct connections")
    print("   2. MCP dev mode may need specific setup for inspector")
    print("   3. Inspector typically connects via HTTP/WebSocket, not STDIO")
    print("   4. Check if dev server starts HTTP server on port 3000")
    
    print(f"\n🔧 Recommended Commands to Try (NVM Windows):")
    print("   # Ensure Node.js is active:")
    print("   nvm list")
    print("   nvm use 22.17.0")
    print("   ")
    print("   # Install MCP Inspector globally:")
    print("   npm install -g @modelcontextprotocol/inspector")
    print("   ")
    print("   # Test MCP Inspector:")
    print("   npx @modelcontextprotocol/inspector python mcp_server.py")
    print("   ")
    print("   # Direct STDIO test (always works):")
    print("   python client.py")
    print("   ")
    print("   # Alternative MCP dev:")
    print("   C:\\Users\\yingdingwang\\Documents\\VENV\\azfdymcp3.12uv\\Scripts\\mcp.exe dev mcp_server.py")

if __name__ == "__main__":
    test_mcp_inspector_connection()
