# python 3.11
# postgre db
# schema creation is done only for new databases, otherwise, automatic script does not touch it
# i.e: @init.py

import psycopg2
import dotenv 
import os
# from datetime import datetime

from __init__ import Logger
from s3_db.a2_parsing_data import (sql_command_from_json)
from s3_db.a1_connect_fetch import (sensorNodes_dataDict)
from utils.db import (print_dbTables_Values, print_dbTables_Columns)


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


def delete_db_schema(cursor, TABLES_DATA):
    """
    Deletes the existing database schema.
    """
    get_auth_group=list(TABLES_DATA.keys())
    cursor.execute(f"""DROP TABLE IF EXISTS public.beehives_sensornodes, 
                   public.{get_auth_group[0].replace('-', '_')}, 
                   public.{get_auth_group[1].replace('-', '_')}, 
                   public.{get_auth_group[2].replace('-', '_')} 
                   CASCADE;""")
    # cursor.execute(f"""TRUNCATE TABLE beehives_sensornodes, 
    #                {get_auth_group[0].replace('-', '_')}, 
    #                {get_auth_group[1].replace('-', '_')}, 
    #                {get_auth_group[2].replace('-', '_')};""")
    # Add more tables to drop if necessary
    Logger.info("Database schema deleted successfully.")


def db_schema_creation(cursor, del_schema=False):

    # --- Sensor Nodes
    TABLES_DATA=sensorNodes_dataDict()

    # # ---- Deleting Database Schema
    if del_schema:
        Logger.info("Deleting existing database schema...")
        delete_db_schema(cursor, TABLES_DATA)
    else:
        Logger.info("Skipping deletion of existing database schema...")

    # ================= Create DB Schema ==================
    # --- Beehives_Sensornodes
    cursor.execute(
        beehives_sensornodes_table()
    )

    # --- Create each Sensor Node Table
    for k, v in TABLES_DATA.items():
        # --- s2120 , d23-lb , s31-lb
        cursor.execute(sql_command_from_json(table_name=k, json_data=v))

    # --- Verify DataBase
    print_dbTables_Columns(cursor)
    Logger.info("Database schema created successfully.")


def db_schema_verification(cursor):
    # =============== Verify DataBase ==================
    # --- Print beehives_sensornodes
    print_dbTables_Values(cursor)

