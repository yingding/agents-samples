# Minimal MCP Client for debugging
import json
import subprocess
import sys
import time

def test_minimal():
    """Minimal test with maximum debugging"""
    print("🔍 Minimal MCP Client Test")
    print("=" * 40)
    
    # Start server
    print("Starting server...")
    process = subprocess.Popen(
        ["uv", "run", "python", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0  # Unbuffered
    )
    
    try:
        # Wait for server to start
        time.sleep(1)
        
        # Check if server is running
        if process.poll() is not None:
            stdout, stderr = process.communicate()
            print(f"❌ Server died immediately!")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return
        
        print("✅ Server appears to be running")
        
        # Send initialize
        print("\nSending initialize...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "minimal-test",
                    "version": "1.0.0"
                }
            }
        }
        
        request_str = json.dumps(init_request) + '\n'
        print(f"Request: {request_str.strip()}")
        
        process.stdin.write(request_str)
        process.stdin.flush()
        
        # Read response
        print("Waiting for response...")
        response_line = process.stdout.readline()
        print(f"Raw response: '{response_line}'")
        
        if response_line:
            try:
                response = json.loads(response_line.strip())
                print(f"Parsed response: {response}")
                
                # If initialize worked, try listing tools
                if "result" in response:
                    print("\nTrying to list tools...")
                    tools_request = {
                        "jsonrpc": "2.0",
                        "id": 2,
                        "method": "tools/list"
                    }
                    
                    tools_str = json.dumps(tools_request) + '\n'
                    print(f"Tools request: {tools_str.strip()}")
                    
                    process.stdin.write(tools_str)
                    process.stdin.flush()
                    
                    tools_response = process.stdout.readline()
                    print(f"Tools response: {tools_response.strip()}")
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON decode error: {e}")
        else:
            print("❌ No response received")
            # Check if process died
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print(f"Process exited with code: {process.returncode}")
                print(f"STDERR: {stderr}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait()
        print("Server stopped")

if __name__ == "__main__":
    test_minimal()
