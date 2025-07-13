# Very simple client to debug parameter issues
import json
import subprocess
import time

def simple_test():
    """Test with no parameters to see what FastMCP expects"""
    print("🔍 Simple Parameter Debug Test")
    
    process = subprocess.Popen(
        ["uv", "run", "python", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        time.sleep(1)
        
        # Initialize first
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
        
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()
        init_response = process.stdout.readline()
        print(f"Init response: {init_response.strip()}")
        
        # Try tools/list with no params
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        process.stdin.write(json.dumps(tools_request) + '\n')
        process.stdin.flush()
        tools_response = process.stdout.readline()
        print(f"Tools response (no params): {tools_response.strip()}")
        
        # Try tools/list with empty params
        tools_request2 = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/list",
            "params": {}
        }
        
        process.stdin.write(json.dumps(tools_request2) + '\n')
        process.stdin.flush()
        tools_response2 = process.stdout.readline()
        print(f"Tools response (empty params): {tools_response2.strip()}")
        
        # Try a tool call
        tool_call = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "query_data",
                "arguments": {
                    "sql": "SELECT COUNT(*) FROM titanic"
                }
            }
        }
        
        process.stdin.write(json.dumps(tool_call) + '\n')
        process.stdin.flush()
        tool_response = process.stdout.readline()
        print(f"Tool call response: {tool_response.strip()}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if process.poll() is None:
            process.terminate()
            process.wait()

if __name__ == "__main__":
    simple_test()
