import sqlite3
import pandas as pd
import os
from .util import get_db_file_path, get_file_path

def init_db():
    """Initialize the SQLite database with a sample table."""
    # load the ./data/titanic_train.csv file into the database
    # create a new SQLite database and load the Titanic dataset in ./data/database.db
    
    db_path = get_db_file_path()
    file_path = get_file_path()
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path))

    with sqlite3.connect(db_path) as conn:
        df = pd.read_csv(file_path)
        df.to_sql("titanic", conn, if_exists="replace", index=False)

def get_first_row():
    """Get the first row of the Titanic dataset."""
    
    db_path = get_db_file_path()
    row = ""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM titanic LIMIT 1")
        row = cursor.fetchone()
    return row

def get_schema(table_name: str) -> str:
    """Get the schema of a specific table."""
    
    db_path = get_db_file_path()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        schema = cursor.fetchall()
    # return schema
    # return "\n".join([f"{col[1]}: {col[2]}" for col in schema])
    return ", ".join([f"{col[1]}: {col[2]}" for col in schema])

if __name__ == "__main__":
    init_db()
    print(get_first_row())
    print(get_schema("titanic"))