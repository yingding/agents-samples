#!/usr/bin/env python3
# MCP Inspector Test Script
# Test connecting to MCP server with inspector

import subprocess
import time
import sys
import os

def test_mcp_with_inspector():
    """Test MCP server with inspector connection"""
    print("🔍 Testing MCP Server with Inspector")
    print("=" * 40)
    
    venv_python = r"C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe"
    
    # Test different server configurations
    servers_to_test = [
        ("Basic MCP Server", "mcp_server.py"),
        ("Enhanced MCP Server", "mcp_server_enhanced.py")
    ]
    
    for server_name, server_script in servers_to_test:
        print(f"\n{'='*20}")
        print(f"Testing: {server_name}")
        print(f"Script: {server_script}")
        print(f"{'='*20}")
        
        if not os.path.exists(server_script):
            print(f"   ❌ {server_script} not found, skipping...")
            continue
        
        # Method 1: Test with npx inspector (if available)
        print("1. Testing with npx MCP inspector...")
        try:
            # Check if Node.js is available
            node_check = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
            if node_check.returncode == 0:
                print(f"   ✅ Node.js available: {node_check.stdout.strip()}")
                
                # Try to run MCP inspector
                print("   📤 Starting MCP inspector...")
                inspector_cmd = [
                    "npx", "--yes", "@modelcontextprotocol/inspector",
                    venv_python, server_script
                ]
                
                print(f"   🔧 Command: {' '.join(inspector_cmd)}")
                
                # Start inspector process
                process = subprocess.Popen(
                    inspector_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.getcwd()
                )
                
                # Wait a moment to see if it starts
                time.sleep(5)
                
                if process.poll() is None:
                    print("   ✅ MCP Inspector appears to be running")
                    print("   🌐 Should be available at: http://localhost:3000")
                    print("   ⏹️  Press Ctrl+C to stop the inspector")
                    
                    # Let it run for a moment then stop for testing
                    time.sleep(2)
                    process.terminate()
                    process.wait(timeout=5)
                    print("   🛑 Inspector stopped for testing")
                else:
                    print(f"   ❌ Inspector exited with code: {process.returncode}")
                    stdout, stderr = process.communicate()
                    if stdout:
                        print(f"   📝 STDOUT: {stdout[:300]}...")
                    if stderr:
                        print(f"   📝 STDERR: {stderr[:300]}...")
                        
            else:
                print("   ❌ Node.js not available for inspector test")
                
        except Exception as e:
            print(f"   ❌ Inspector test failed: {e}")
        
        # Method 2: Test with MCP dev command
        print("\n2. Testing with MCP dev command...")
        try:
            mcp_exe = r"C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\mcp.exe"
            
            if os.path.exists(mcp_exe):
                print(f"   📤 Running: {mcp_exe} dev {server_script}")
                
                process = subprocess.Popen(
                    [mcp_exe, "dev", server_script],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=os.getcwd()
                )
                
                time.sleep(3)
                
                if process.poll() is None:
                    print("   ✅ MCP dev server running")
                    
                    # Check if port 3000 is accessible
                    try:
                        import urllib.request
                        response = urllib.request.urlopen("http://localhost:3000", timeout=3)
                        print("   ✅ Web interface accessible at http://localhost:3000")
                    except Exception:
                        print("   ⚠️  Web interface not accessible on port 3000")
                    
                    process.terminate()
                    process.wait(timeout=5)
                    print("   🛑 MCP dev server stopped")
                else:
                    print(f"   ❌ MCP dev exited with code: {process.returncode}")
                    stdout, stderr = process.communicate()
                    if stdout:
                        print(f"   📝 STDOUT: {stdout[:200]}...")
                    if stderr:
                        print(f"   📝 STDERR: {stderr[:200]}...")
            else:
                print(f"   ❌ MCP executable not found: {mcp_exe}")
                
        except Exception as e:
            print(f"   ❌ MCP dev test failed: {e}")
        
        # Method 3: Direct STDIO test (always works)
        print("\n3. Testing direct STDIO connection...")
        try:
            process = subprocess.Popen(
                [venv_python, server_script],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=os.getcwd()
            )
            
            if process.poll() is None:
                print("   ✅ Direct STDIO server running")
                process.terminate()
                process.wait()
                print("   🛑 STDIO server stopped")
            else:
                print(f"   ❌ STDIO server failed to start")
                
        except Exception as e:
            print(f"   ❌ STDIO test failed: {e}")
    
    print(f"\n{'='*40}")
    print("🎯 MCP Inspector Connection Summary:")
    print("")
    print("✅ Working Methods:")
    print("   • Direct STDIO: python mcp_server.py")
    print("   • Python client: python client.py")
    print("")
    print("⚠️  Inspector Methods (may need setup):")
    print("   • npx @modelcontextprotocol/inspector python mcp_server.py")
    print("   • mcp dev mcp_server.py")
    print("")
    print("🔧 If Inspector Not Working:")
    print("   1. Ensure Node.js is installed")
    print("   2. Check firewall/port 3000 access")
    print("   3. Try enhanced server: python mcp_server_enhanced.py")
    print("   4. Use direct testing: python client.py")

if __name__ == "__main__":
    test_mcp_with_inspector()
