# MCP Client - Test the FastMCP Server
# This client connects to the MCP server via STDIO and tests available tools/resources

import json
import subprocess
import sys
from typing import Dict, Any

class MCPClient:
    def __init__(self, server_command: list):
        """Initialize MCP client with server command"""
        self.server_command = server_command
        self.process = None
        self.request_id = 1

    def start_server(self):
        """Start the MCP server process"""
        try:
            self.process = subprocess.Popen(
                self.server_command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0
            )
            print(f"✅ MCP Server started with command: {' '.join(self.server_command)}")
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            sys.exit(1)

    def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send JSON-RPC request to server"""
        if not self.process:
            raise RuntimeError("Server not started")

        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method
        }
        if params:
            request["params"] = params

        self.request_id += 1

        # Send request
        request_json = json.dumps(request) + '\n'
        print(f"📤 Sending: {method}")
        self.process.stdin.write(request_json)
        self.process.stdin.flush()

        # Read response
        response_line = self.process.stdout.readline()
        if not response_line:
            raise RuntimeError("No response from server")

        try:
            response = json.loads(response_line.strip())
            print(f"📥 Response: {response.get('result', response.get('error', 'Unknown'))}")
            return response
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON response: {response_line}")
            raise

    def initialize(self):
        """Initialize the MCP connection"""
        return self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {
                    "listChanged": True
                },
                "sampling": {}
            },
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })

    def list_tools(self):
        """List available tools"""
        return self.send_request("tools/list")

    def list_resources(self):
        """List available resources"""
        return self.send_request("resources/list")

    def call_tool(self, name: str, arguments: Dict[str, Any]):
        """Call a specific tool"""
        return self.send_request("tools/call", {
            "name": name,
            "arguments": arguments
        })

    def read_resource(self, uri: str):
        """Read a specific resource"""
        return self.send_request("resources/read", {
            "uri": uri
        })

    def stop_server(self):
        """Stop the MCP server"""
        if self.process:
            self.process.terminate()
            self.process.wait()
            print("🛑 Server stopped")

def test_mcp_server():
    """Test the MCP server functionality"""
    # Server command - using PowerShell to call mcp.ps1
    server_cmd = [
        "powershell.exe", 
        "-ExecutionPolicy", "Bypass", 
        "-File", "mcp.ps1", 
        "server"
    ]

    client = MCPClient(server_cmd)
    
    try:
        print("🚀 Testing MCP Server via STDIO")
        print("=" * 50)
        
        # Start server
        client.start_server()
        
        # Initialize connection
        print("\n1️⃣ Initializing connection...")
        init_response = client.initialize()
        if "error" in init_response:
            print(f"❌ Initialization failed: {init_response['error']}")
            return
        
        # List tools
        print("\n2️⃣ Listing available tools...")
        tools_response = client.list_tools()
        if "result" in tools_response:
            tools = tools_response["result"].get("tools", [])
            for tool in tools:
                print(f"   🔧 {tool['name']}: {tool.get('description', 'No description')}")
        
        # List resources
        print("\n3️⃣ Listing available resources...")
        resources_response = client.list_resources()
        if "result" in resources_response:
            resources = resources_response["result"].get("resources", [])
            for resource in resources:
                print(f"   📁 {resource['uri']}: {resource.get('name', 'No name')}")
        
        # Test sum tool
        print("\n4️⃣ Testing sum tool...")
        sum_response = client.call_tool("sum", {"a": 5, "b": 3})
        if "result" in sum_response:
            result = sum_response["result"]["content"][0]["text"]
            print(f"   ✅ sum(5, 3) = {result}")
        
        # Test greeting resource
        print("\n5️⃣ Testing greeting resource...")
        greeting_response = client.read_resource("greeting://World")
        if "result" in greeting_response:
            contents = greeting_response["result"]["contents"]
            for content in contents:
                print(f"   ✅ greeting://World = {content['text']}")
        
        print("\n✅ All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        client.stop_server()

if __name__ == "__main__":
    test_mcp_server()
