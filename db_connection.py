from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection parameters
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
HOST = os.getenv("DB_HOST")
DATABASE = os.getenv("DB_NAME")

# Create SQLAlchemy engine
DATABASE_URL = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}/{DATABASE}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    """Creates a new database session and closes it after use."""
    session = SessionLocal()
    return session  # Not using yield to avoid generator issues

def fetch_table_data(table_name):
    """Fetches data from the specified table."""
    try:
        with engine.connect() as connection:
            df = pd.read_sql(f"SELECT * FROM {table_name}", connection)
        return df
    except Exception as e:
        print(f"Error fetching data from {table_name}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on failure
