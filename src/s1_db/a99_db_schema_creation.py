# python 3.11
# postgre db
# schema creation is done only for new databases, otherwise, automatic script does not touch it
# i.e: @init.py

import psycopg2
import requests
import dotenv 
import os
from datetime import datetime
import pandas as pd

from src.s1_db.a2_parsing_data import (sql_command_from_json)
from src.s1_db.a1_connect_fetch import (sensorNodes_dataDict)

def print_dbTables_Columns(cursor):
    # ----- @Perplexity -----
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


def print_dbTables_Values(cursor):
    cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public';
    """)
    tables = cursor.fetchall()

    for (table_name,) in tables:
        print(f"Table: {table_name}")
        # Get column names for each table
        cursor.execute(f"""
            SELECT * FROM {table_name};
        """)
        df=pd.DataFrame(columns=[des[0] for des in cursor.description],
                        data=cursor.fetchall())
        print(df)
        print()


def beehives_sensornodes_table():
    return """
        CREATE TABLE IF NOT EXISTS beehives_sensornodes(
            sensor_node_id SERIAL PRIMARY KEY,
            bee_hive VARCHAR(100),
            sensor_node_name VARCHAR(100),
            sensor_node_type VARCHAR(100),
            sensor_node_entityId VARCHAR(100),
            time_of_entry timestamp NOT NULL
        )
        """


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

    # # ================= Create DB Schema ==================
    # # --- Sensor Nodes
    # TABLES_DATA=sensorNodes_dataDict()

    # # # ---- Deleting Database Schema
    # # get_auth_group=list(TABLES_DATA.keys())
    # # cursor.execute(f"""DROP TABLE IF EXISTS beehives_sensornodes, 
    # #                {get_auth_group[0].replace('-', '_')}, 
    # #                {get_auth_group[1].replace('-', '_')}, 
    # #                {get_auth_group[2].replace('-', '_')} 
    # #                CASCADE;""")

    # # --- Beehives_Sensornodes
    # cursor.execute(
    #     beehives_sensornodes_table()
    # )

    # # --- Create each Sensor Node Table
    # for k, v in TABLES_DATA.items():
    #     # --- s2120 , d23-lb , s31-lb
    #     cursor.execute(sql_command_from_json(table_name=k, json_data=v))

    # # --- Verify DataBase
    # print_dbTables_Columns(cursor)

    # =============== Verify DataBase ==================
    # --- Print beehives_sensornodes
    print_dbTables_Values(cursor)

    # --- Close Database Connection at the End
    conn.commit()
    cursor.close()
    conn.close()

