# python 3.12
# postgresSQL

import os
import psycopg2
from dotenv import load_dotenv

import __init__
from __init__ import Logger
from s2_configure.db import db_connection, db_connection_close
from s3_db.a1_connect_fetch import sensorNodes_dataDict
from s3_db.a98_db_beehives_update import (read_beehives_sensornodes_json,
                                           trigger_automatic_db_schema_update,
                                           db_beehives_table_update)
from s3_db.a99_db_schema_creation import (db_schema_creation, db_schema_verification)
from s4_collect.b1_fill_sensor_node_tables import filling_tables_with_sensor_measured_values

# def beehappy_db_schema_setup():
#     pass


# def beehappy_db_beehives_update():
#     pass


def is_schema_empty(cursor):
    """
    Check if the database schema is empty.
    """
    # This query works for PostgreSQL
    cursor.execute("""
        SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    count = cursor.fetchone()[0]
    return count == 0

def beehappy_data_collection():
    """
    1. check if schema is existed, not create it
    2. update the beehives table, which contains the meta data of the sensor nodes- combines physical and virtual sensor nodes
    3. if all is good, then start filling tables
    4. repeat this for every 5 minutes
    """
    conn= db_connection()
    if not conn:
        Logger.error("Failed to connect to the database.")
        return
    cursor = conn.cursor()

    if is_schema_empty(cursor):
        Logger.info("Database schema is empty. Creating tables.")
        db_schema_creation(cursor, del_schema=False)
        db_schema_verification(cursor)
        db_beehives_table_update(cursor)
    else:
        Logger.info("Database schema exists. Filling tables with values.")

    # --- Beehappy Data Collection Workflow ---
    try:
        beehives_json_dict=read_beehives_sensornodes_json()
        api_json_dict=sensorNodes_dataDict()
    except Exception as e:  
        Logger.error(f"Error during data collection: {e}")
        db_connection_close(conn, cursor)
        return
    else:

        trigger_automatic_db_schema_update(cursor=cursor, 
                                        beehives_json_dict=beehives_json_dict, 
                                        api_json_dict=api_json_dict)
        filling_tables_with_sensor_measured_values(cursor)

        # --- Close Database Connection at the End
        db_connection_close(conn, cursor)

def beehappy_db_clean_createschema():
    """
    1. check if schema is existed, not create it
    2. update the beehives table, which contains the meta data of the sensor nodes- combines physical and virtual sensor nodes
    3. if all is good, then start filling tables
    4. repeat this for every 5 minutes
    """
    conn= db_connection()
    if not conn:
        Logger.error("Failed to connect to the database.")
        return
    cursor = conn.cursor()

    # --- Beehappy Data Base Clean Up and Reconfigure Workflow ---
    db_schema_creation(cursor, del_schema=True)
    db_schema_verification(cursor)
    db_beehives_table_update(cursor)

    Logger.info("Database schema deleted. Recreated again and beehives table filled.")

    # --- Close Database Connection at the End
    db_connection_close(conn, cursor)