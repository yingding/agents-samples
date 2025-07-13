# Simple test to check if the MCP server starts correctly
import subprocess
import sys
import time
import os
import json

def test_server_startup():
    """Test if the server can start without errors"""
    print("🔧 Testing MCP Server Startup")
    print("=" * 50)
    
    # Test 1: Check if server starts with direct Python
    print("\n1️⃣ Testing direct Python execution...")
    try:
        process = subprocess.Popen(
            ["uv", "run", "python", "mcp_server.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=r"C:\Users\yingdingwang\Documents\VCS\democollections\agents-samples\02sqlmcp"
        )
        
        # Wait a moment for startup
        time.sleep(2)
        
        # Check if process is still running
        if process.poll() is None:
            print("   ✅ Server started successfully")
            
            # Try sending a simple initialize message
            print("   📤 Sending initialize message...")
            init_msg = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "1.0.0"}
                }
            }
            
            process.stdin.write(json.dumps(init_msg) + '\n')
            process.stdin.flush()
            
            # Try to read response
            try:
                response = process.stdout.readline()
                if response:
                    print(f"   📥 Got response: {response.strip()}")
                else:
                    print("   ❌ No response received")
            except Exception as e:
                print(f"   ⚠️  Error reading response: {e}")
            
            # Clean shutdown
            process.terminate()
            process.wait()
            
        else:
            # Process exited, check why
            stdout, stderr = process.communicate()
            print(f"   ❌ Server exited immediately")
            print(f"   STDOUT: {stdout}")
            print(f"   STDERR: {stderr}")
            
    except Exception as e:
        print(f"   ❌ Failed to start server: {e}")
    
    # Test 2: Check database file
    print("\n2️⃣ Testing database file...")
    db_path = r"C:\Users\yingdingwang\Documents\VCS\democollections\agents-samples\02sqlmcp\data\database.db"
    if os.path.exists(db_path):
        print(f"   ✅ Database file exists: {db_path}")
        
        # Test database connection
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            print(f"   ✅ Database accessible, tables: {[t[0] for t in tables]}")
            conn.close()
        except Exception as e:
            print(f"   ❌ Database error: {e}")
    else:
        print(f"   ❌ Database file missing: {db_path}")
        print("   💡 Try running: python init_sqlite.py")
    
    # Test 3: Check PowerShell launcher
    print("\n3️⃣ Testing PowerShell launcher...")
    if os.path.exists("mcp.ps1"):
        try:
            process = subprocess.Popen(
                ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", "mcp.ps1", "server"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=r"C:\Users\yingdingwang\Documents\VCS\democollections\agents-samples\02sqlmcp"
            )
            
            time.sleep(3)
            
            if process.poll() is None:
                print("   ✅ PowerShell launcher started server")
                process.terminate()
                process.wait()
            else:
                stdout, stderr = process.communicate()
                print(f"   ❌ PowerShell launcher failed")
                print(f"   STDOUT: {stdout}")
                print(f"   STDERR: {stderr}")
                
        except Exception as e:
            print(f"   ❌ PowerShell test failed: {e}")
    else:
        print("   ⚠️  mcp.ps1 not found")
    
    # Test 4: Check Python environment
    print("\n4️⃣ Testing Python environment...")
    try:
        import mcp.server.fastmcp
        print("   ✅ FastMCP module available")
    except ImportError as e:
        print(f"   ❌ FastMCP import error: {e}")
        print("   💡 Try: pip install mcp")

if __name__ == "__main__":
    test_server_startup()
