# MCP Test Suite - Comprehensive testing of FastMCP Server
# Tests all available tools and resources via STDIO

import json
import subprocess
import sys
import time
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'

def print_colored(text, color):
    print(f"{color}{text}{Colors.RESET}")

def run_mcp_test():
    """Run comprehensive MCP server test"""
    print_colored("🧪 MCP Server Test Suite", Colors.CYAN)
    print_colored("=" * 40, Colors.CYAN)
    
    # Test cases
    tests = [
        {
            "name": "Initialize Connection",
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-suite", "version": "1.0.0"}
            }
        },
        {
            "name": "List Tools",
            "method": "tools/list",
            "params": {}
        },
        {
            "name": "List Resources", 
            "method": "resources/list",
            "params": {}
        },
        {
            "name": "Call Sum Tool",
            "method": "tools/call",
            "params": {
                "name": "sum",
                "arguments": {"a": 10, "b": 25}
            }
        },
        {
            "name": "Read Greeting Resource",
            "method": "resources/read", 
            "params": {
                "uri": "greeting://TestUser"
            }
        }
    ]
    
    # Start server
    cmd = ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "mcp.ps1", "server"]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            bufsize=0
        )
        
        print_colored("✅ MCP Server started", Colors.GREEN)
        time.sleep(1)  # Give server time to start
        
        # Run each test
        for i, test in enumerate(tests, 1):
            print(f"\n{i}️⃣ Testing: {test['name']}")
            
            request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": test["method"],
                "params": test["params"]
            }
            
            # Send request
            request_json = json.dumps(request) + '\n'
            process.stdin.write(request_json)
            process.stdin.flush()
            
            # Read response
            try:
                response_line = process.stdout.readline()
                if response_line:
                    response = json.loads(response_line.strip())
                    
                    if "result" in response:
                        print_colored(f"   ✅ Success", Colors.GREEN)
                        
                        # Show specific results
                        result = response["result"]
                        if test["method"] == "tools/list":
                            tools = result.get("tools", [])
                            for tool in tools:
                                print(f"      🔧 {tool.get('name')}: {tool.get('description')}")
                        
                        elif test["method"] == "resources/list":
                            resources = result.get("resources", [])
                            for resource in resources:
                                print(f"      📁 {resource.get('uri')}")
                        
                        elif test["method"] == "tools/call":
                            if "content" in result:
                                content = result["content"][0]["text"]
                                print(f"      📊 Result: {content}")
                        
                        elif test["method"] == "resources/read":
                            if "contents" in result:
                                for content in result["contents"]:
                                    print(f"      📄 Content: {content.get('text')}")
                        
                        elif test["method"] == "initialize":
                            server_info = result.get("serverInfo", {})
                            print(f"      🖥️ Server: {server_info.get('name')} v{server_info.get('version')}")
                            
                    else:
                        error = response.get("error", {})
                        print_colored(f"   ❌ Error: {error.get('message', 'Unknown error')}", Colors.RED)
                        
                else:
                    print_colored(f"   ❌ No response received", Colors.RED)
                    
            except json.JSONDecodeError as e:
                print_colored(f"   ❌ Invalid JSON response: {e}", Colors.RED)
            except Exception as e:
                print_colored(f"   ❌ Error: {e}", Colors.RED)
        
        # Summary
        print(f"\n{Colors.CYAN}{'=' * 40}{Colors.RESET}")
        print_colored("🎉 Test Suite Completed", Colors.GREEN)
        print_colored("🔧 Available Tools: sum(a, b)", Colors.YELLOW)
        print_colored("📁 Available Resources: greeting://{name}", Colors.YELLOW)
        
    except Exception as e:
        print_colored(f"❌ Failed to start server: {e}", Colors.RED)
    finally:
        if 'process' in locals():
            process.terminate()
            process.wait()
            print_colored("🛑 Server stopped", Colors.BLUE)

if __name__ == "__main__":
    run_mcp_test()
