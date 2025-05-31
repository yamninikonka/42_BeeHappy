# python 3.11
# postgre db

import psycopg2
import requests
import dotenv 
import os
import json
from datetime import datetime
from automatic_data_fetch import all_node_types
from db_schema import print_db_tables

# abs_path = os.path.abspath(".")
cwd = os.getcwd()
now = datetime.now().replace(microsecond=0)

def read_json(j_file=cwd+"/src/data/beehives_sensors_v2.json"):
    with open(j_file) as j:
        json_dict = json.load(j)

    return json_dict

def preparing_data(json_dict):
    data = []
    for k, v in json_dict.items():
        each_value = (k, v[0], "LoRa-"+v[1])
        data.append(each_value)
    return data

def automatic_update_from_json(cursor):
    # -- automatic update of the sensor names from json file
    sql = "INSERT INTO beehives_sensornodes (sensor_node_id, bee_hive, sensor_node_name, time_of_entry) VALUES (%s, %s, %s, NOW())"

    # List of tuples: each tuple is a row to insert
    values = preparing_data(read_json())

    # Insert multiple rows
    cursor.executemany(sql, values)
    
def filling_sensor_types_upon_condition(cursor):
    # -- filling sensor node based on sensor name
    for name, type_value in all_node_types().items():
        cursor.execute(
            "UPDATE beehives_sensornodes SET sensor_node_type = %s WHERE sensor_node_name = %s",
            (type_value, name)
        )

def db_table_update():
    # print(preparing_data(read_json()))
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

    # -------------- Filling Database Table -------------------
    # # --- Beehives_Sensornodes Filling Values ---
    automatic_update_from_json(cursor)

    # # --- Filling based on Condition ---
    filling_sensor_types_upon_condition(cursor)

    # print_db_tables(cursor)

    conn.commit()
    cursor.close()
    conn.close()

