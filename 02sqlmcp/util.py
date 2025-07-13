import os 

def get_db_file_path():
    """Get the path to the SQLite database file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "data", "database.db")

def get_file_path():
    """Get the path to the Titanic dataset CSV file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, "data", "titanic_train.csv")