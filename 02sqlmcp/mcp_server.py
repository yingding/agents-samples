import sqlite3

from mcp.server.fastmcp import FastMCP
# from util import get_db_file_path

mcp = FastMCP("SQLite Explorer")
# DB_PATH = get_db_file_path("sqlite_explorer.db")
DB_PATH = "C:\\Users\\yingdingwang\\Documents\\VCS\\democollections\\agents-samples\\02sqlmcp\\data\\database.db"

@mcp.resource("schema://main")
def get_schema() -> str:
    """Provide the database schema as a resource"""
    conn = sqlite3.connect(DB_PATH)
    schema = conn.execute("SELECT sql FROM sqlite_master WHERE type='table'").fetchall()
    return "\n".join(sql[0] for sql in schema if sql[0])


@mcp.tool()
def query_data(sql: str) -> str:
    """Execute SQL queries safely"""
    conn = sqlite3.connect(DB_PATH)
    try:
        result = conn.execute(sql).fetchall()
        return "\n".join(str(row) for row in result)
    except Exception as e:
        return f"Error: {str(e)}"