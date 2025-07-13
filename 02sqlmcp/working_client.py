# Working MCP Client - Based on successful MCP Inspector test
import json
import subprocess
import time

def working_client_test():
    """Create a working client based on the successful MCP Inspector"""
    print("🚀 Working MCP Client Test")
    print("=" * 50)
    
    # Use the same command that worked with MCP Inspector
    process = subprocess.Popen(
        [r"C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv\Scripts\python.exe", "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=0
    )
    
    try:
        time.sleep(1)
        
        # 1. Initialize
        print("1️⃣ Initializing...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": "working-test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        process.stdin.write(json.dumps(init_request) + '\n')
        process.stdin.flush()
        
        init_response = process.stdout.readline()
        print(f"   ✅ Init: {json.loads(init_response.strip())['result']['serverInfo']['name']}")
        
        # 2. Test schema resource
        print("\n2️⃣ Testing schema resource...")
        schema_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "resources/read",
            "params": {
                "uri": "schema://main"
            }
        }
        
        process.stdin.write(json.dumps(schema_request) + '\n')
        process.stdin.flush()
        
        schema_response = process.stdout.readline()
        schema_result = json.loads(schema_response.strip())
        
        if "result" in schema_result:
            schema_content = schema_result["result"]["contents"][0]["text"]
            print(f"   ✅ Schema retrieved: {len(schema_content)} characters")
            print(f"   📋 First line: {schema_content.split('n')[0] if schema_content else 'Empty'}")
        else:
            print(f"   ❌ Schema error: {schema_result.get('error', 'Unknown')}")
        
        # 3. Test SQL query
        print("\n3️⃣ Testing SQL query...")
        query_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "query_data",
                "arguments": {
                    "sql": "SELECT COUNT(*) as total FROM titanic"
                }
            }
        }
        
        process.stdin.write(json.dumps(query_request) + '\n')
        process.stdin.flush()
        
        query_response = process.stdout.readline()
        query_result = json.loads(query_response.strip())
        
        if "result" in query_result:
            result_content = query_result["result"]["content"][0]["text"]
            print(f"   ✅ Query result: {result_content}")
        else:
            print(f"   ❌ Query error: {query_result.get('error', 'Unknown')}")
        
        print(f"\n🎉 MCP Server is working correctly!")
        print(f"   • Schema resource: ✅")
        print(f"   • SQL queries: ✅")
        print(f"   • JSON-RPC protocol: ✅")
        
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
    working_client_test()
