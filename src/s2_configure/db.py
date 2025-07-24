
from dotenv import load_dotenv
import os
import psycopg2

from __init__ import Logger, pkg_path


# Security
# Load .env from the "config" subfolder
dotenv_path = os.path.join(pkg_path, 'project', '.env')
load_dotenv(dotenv_path)
# load_dotenv() # dotenv_path=Path("../src/data/.env")
api_key = os.getenv("API_KEY")
db_password = os.getenv("DB_PASSWORD")

# Connection to Server using HTTP Request
base_url = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/"


def db_connection():
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        # # Database credentials
        # load_dotenv()
        # db_password = os.getenv("DB_PASSWORD")

        # Database connection
        conn = psycopg2.connect(
            host="d71a3071-7535-48f1-8b24-d3887122b6a1.postgresql.eu01.onstackit.cloud",
            database="beehappydb3",
            user="beehappyuser3",
            password=db_password,
            port="5432"
        )
        return conn
    except Exception as e:
        Logger.error(f"Database connection failed: {e}")
        raise e
    
def db_connection_close(conn, cursor):
    """
    Closes the database connection and cursor.
    """
    try:
        cursor.close()
        conn.close()
        Logger.info("Database connection closed successfully.")
    except Exception as e:
        Logger.error(f"Failed to close database connection: {e}")
        