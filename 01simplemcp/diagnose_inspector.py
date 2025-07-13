#!/usr/bin/env python3
# MCP Inspector Diagnostic Script
# Check what's wrong with the MCP inspector setup

import subprocess
import os
import sys

def check_mcp_inspector():
    """Diagnose MCP inspector issues"""
    print("🔍 MCP Inspector Diagnostic")
    print("=" * 40)
    
    venv_path = r"C:\Users\yingdingwang\Documents\VENV\azfdymcp3.12uv"
    scripts_path = os.path.join(venv_path, "Scripts")
    
    # Check executables
    print("1. Checking available executables...")
    executables = ["mcp.exe", "fastmcp.exe", "python.exe"]
    
    for exe in executables:
        exe_path = os.path.join(scripts_path, exe)
        if os.path.exists(exe_path):
            print(f"   ✅ {exe} found")
            
            # Try to get version/help
            try:
                result = subprocess.run(
                    [exe_path, "--help"], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                print(f"      📊 Exit code: {result.returncode}")
                if result.stdout:
                    lines = result.stdout.split('\n')[:3]  # First 3 lines
                    print(f"      📝 Output preview: {' '.join(lines)}")
                if result.stderr:
                    print(f"      ⚠️  Error: {result.stderr[:100]}...")
                    
            except subprocess.TimeoutExpired:
                print(f"      ⏱️  Timeout - {exe} may be hanging")
            except Exception as e:
                print(f"      ❌ Error running {exe}: {e}")
        else:
            print(f"   ❌ {exe} not found")
    
    # Test MCP dev command specifically
    print("\n2. Testing MCP dev command...")
    mcp_exe = os.path.join(scripts_path, "mcp.exe")
    server_script = os.path.join(os.getcwd(), "mcp_server.py")
    
    if os.path.exists(mcp_exe) and os.path.exists(server_script):
        try:
            print("   📤 Running: mcp.exe dev mcp_server.py")
            result = subprocess.run(
                [mcp_exe, "dev", server_script],
                capture_output=True,
                text=True,
                timeout=5
            )
            print(f"   📊 Exit code: {result.returncode}")
            if result.stdout:
                print(f"   📝 STDOUT: {result.stdout[:200]}...")
            if result.stderr:
                print(f"   ⚠️  STDERR: {result.stderr[:200]}...")
                
        except subprocess.TimeoutExpired:
            print("   ⏱️  MCP dev command timed out (may be running)")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    else:
        print("   ❌ Missing mcp.exe or mcp_server.py")
    
    # Check if Node.js is available for MCP Inspector
    print("\n3. Checking Node.js for MCP Inspector...")
    try:
        result = subprocess.run(
            ["node", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"   ✅ Node.js version: {result.stdout.strip()}")
        else:
            print("   ❌ Node.js not found or error")
    except Exception as e:
        print(f"   ❌ Node.js check failed: {e}")
    
    # Check if npx and MCP Inspector are available
    print("\n4. Checking MCP Inspector availability...")
    try:
        result = subprocess.run(
            ["npx", "@modelcontextprotocol/inspector", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"   ✅ MCP Inspector available")
        else:
            print("   ❌ MCP Inspector not available via npx")
            print(f"      Exit code: {result.returncode}")
            if result.stderr:
                print(f"      Error: {result.stderr[:100]}...")
    except Exception as e:
        print(f"   ❌ npx/MCP Inspector check failed: {e}")
    
    print(f"\n{'='*40}")
    print("🎯 Diagnostic Summary:")
    print("   - MCP executables: Check individual status above")
    print("   - Dev mode: May have display/output issues")
    print("   - Inspector: Requires Node.js + @modelcontextprotocol/inspector")
    print("   - Recommendation: Use STDIO server mode for reliable operation")
    
    print(f"\n🔧 Working Commands:")
    print("   python mcp_server.py           # Direct STDIO server")
    print("   .\\mcp.ps1 server             # PowerShell launcher")
    print("   python test_simple.py         # Test STDIO communication")

if __name__ == "__main__":
    check_mcp_inspector()
