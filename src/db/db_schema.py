# python 3.11
# postgre db

import psycopg2
import requests
import dotenv 
import os
from datetime import datetime
from automatic_data_fetch import sql_command_from_json, get_auth_group

def print_db_tables(cursor):
    # cursor.execute("""
    # DROP TABLE IF EXISTS names CASCADE;
    # """)
    # Get all table names in the public schema
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public';
    """)
    tables = cursor.fetchall()

    for (table_name,) in tables:
        print(f"Table: {table_name}")
        # Get column names for each table
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s;
        """, (table_name,))
        columns = cursor.fetchall()
        for (column_name,) in columns:
            print(f"    Column: {column_name}")
        print()


def db_schema_creation():
    # For Security the credentials to access DB are read from an .env file
    dotenv.load_dotenv()
    db_password = os.getenv("DB_PASSWORD")

    # Database connection
    try:
        conn = psycopg2.connect(
            host="d71a3071-7535-48f1-8b24-d3887122b6a1.postgresql.eu01.onstackit.cloud",
            database="beehappydb3",
            user="beehappyuser3",
            password=db_password,
            port="5432"
        )
    except Exception as e:
        raise e
    else:
        cursor = conn.cursor()

    # Creating Database Schema
    # cursor.execute(f"""DROP TABLE IF EXISTS beehives_sensornodes, 
    #                {get_auth_group(1)[0].replace('-', '_')}, 
    #                {get_auth_group(2)[0].replace('-', '_')}, 
    #                {get_auth_group(3)[0].replace('-', '_')} 
    #                CASCADE;""")
    # --- Beehives_Sensornodes
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS beehives_sensornodes(
            sensor_node_id SERIAL PRIMARY KEY,
            bee_hive VARCHAR(100),
            sensor_node_name VARCHAR(100),
            sensor_node_type VARCHAR(100),
            time_of_entry timestamp NOT NULL
        )
        """
    )
    # --- s2120 
    cursor.execute(sql_command_from_json(1))

    # --- d23-lb
    cursor.execute(sql_command_from_json(2))

    # --- s31-lb
    cursor.execute(sql_command_from_json(3))

    print_db_tables(cursor)

    conn.commit()
    cursor.close()
    conn.close()

