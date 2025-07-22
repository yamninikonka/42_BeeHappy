# python 3.12
# postgresSQL

import os
import numpy
import psycopg2
from dotenv import load_dotenv

import __init__
from src import Logger
from src.s1_db.a1_connect_fetch import sensorNodes_dataDict
from src.s1_db.a98_db_beehives_update import (read_beehives_sensornodes_json,
                                           trigger_automatic_db_schema_update)
from src.collect.fill import filling_tables_with_sensor_measured_values


def beehappy_data_collection():
    """
    1. check tables are existed, if not create
    2. fetch sensor_id for child tables
    3. insert data into child tables
    4. 
    """
    # Database credentials
    load_dotenv()
    db_password = os.getenv("DB_PASSWORD")

    # Database connection
    conn = psycopg2.connect(
                host="d71a3071-7535-48f1-8b24-d3887122b6a1.postgresql.eu01.onstackit.cloud",
                database="beehappydb3",
                user="beehappyuser3",
                password=db_password,
                port="5432"
            )
    cursor = conn.cursor()

    # --- Beehappy Data Collection Workflow ---
    beehives_json_dict=read_beehives_sensornodes_json()
    api_json_dict=sensorNodes_dataDict()
    trigger_automatic_db_schema_update(cursor=cursor, 
                                       beehives_json_dict=beehives_json_dict, 
                                       api_json_dict=api_json_dict)
    filling_tables_with_sensor_measured_values(cursor)

    # --- Close Gracefully
    conn.commit()
    cursor.close()
    conn.close()