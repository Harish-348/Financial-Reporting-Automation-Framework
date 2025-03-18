from db_connection import get_db_session
import queries
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import inspect

def execute_query(query_func):
    """Execute a given SQL query using SQLAlchemy session."""
    session = next(get_db_session())  # Get a session instance
    try:
        session.execute(text(query_func()))  # Execute query
        session.commit()  # Commit changes
        print(f"Query executed successfully: {query_func.__name__}")
    except Exception as e:
        session.rollback()  # Rollback in case of failure
        print(f"Error executing {query_func.__name__}: {e}")
    finally:
        session.close()  # Ensure session is closed

def run_all_queries():
    """Execute all query functions from queries.py dynamically."""
    query_functions = [
        func for name, func in inspect.getmembers(queries, inspect.isfunction)
    ]  # Get all functions from queries.py

    for query_func in query_functions:
        execute_query(query_func)  # Execute each query function

