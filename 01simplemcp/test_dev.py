# Test MCP Dev Server
# Test if the development server starts and responds

import subprocess
import time
import sys
import threading
import json

def test_dev_server():
    """Test the MCP development server"""
    print("🔧 Testing MCP Dev Server")
    print("=" * 30)
    
    # Start dev server
    print("1. Starting dev server...")
    try:
        # Use the PowerShell launcher
        cmd = ["powershell", "-ExecutionPolicy", "Bypass", "-File", "mcp.ps1", "dev"]
        
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("   ✅ Dev server process started")
        print(f"   📊 Process ID: {process.pid}")
        
        # Wait a moment for server to initialize
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("   ✅ Dev server is running")
            
            # Try to send a simple request
            print("2. Testing server communication...")
            
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
                process.stdin.write(json.dumps(init_request) + '\n')
                process.stdin.flush()
                print("   📤 Initialize request sent")
                
                # Try to read response with timeout
                import select
                ready, _, _ = select.select([process.stdout], [], [], 3)
                
                if ready:
                    response = process.stdout.readline()
                    if response:
                        print("   📥 Response received from dev server")
                        try:
                            data = json.loads(response.strip())
                            print(f"   ✅ Valid JSON response: {len(response)} chars")
                        except json.JSONDecodeError:
                            print(f"   ⚠️  Non-JSON response: {response[:50]}...")
                    else:
                        print("   ❌ No response received")
                else:
                    print("   ⏱️  Timeout waiting for response")
                    
            except Exception as e:
                print(f"   ❌ Communication error: {e}")
            
        else:
            print(f"   ❌ Dev server exited with code: {process.returncode}")
            stderr = process.stderr.read()
            if stderr:
                print(f"   📝 Error output: {stderr}")
        
        # Clean up
        print("3. Stopping dev server...")
        try:
            process.terminate()
            process.wait(timeout=5)
            print("   ✅ Dev server stopped")
        except subprocess.TimeoutExpired:
            process.kill()
            print("   🔨 Dev server force killed")
            
    except Exception as e:
        print(f"   ❌ Failed to start dev server: {e}")
    
    print(f"\n{'='*30}")
    print("📋 Dev Server Test Summary:")
    print("   - Dev mode uses 'mcp dev' command")
    print("   - Should provide enhanced logging/debugging")
    print("   - May include web inspector on port 3000")
    print("   - Use 'mcp.ps1 inspector' for web interface")

if __name__ == "__main__":
    test_dev_server()
