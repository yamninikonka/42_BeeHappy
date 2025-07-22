# python 3.11
# postgre db

import psycopg2
import requests
import dotenv 
import os
import json
from datetime import datetime

from src.s1_db import Total_Sensor_Node_Types
from src.__init__ import Logger, update_total_sensor_node
from src.s1_db.a1_connect_fetch import (sensorNodes_dataDict)
from src.s1_db.a2_parsing_data import (sql_command_from_json)
from src.s1_db.a4_meta_data import (extract_sensor_nodes_meta_data)
from src.s1_db.a99_db_schema_creation import (print_dbTables_Columns, print_dbTables_Values)

# abs_path = os.path.abspath(".")
cwd = os.getcwd()
# now = datetime.now().replace(microsecond=0)

def read_beehives_sensornodes_json(j_file=cwd+"/src/data/beehives_sensors_v2.json"):
    with open(j_file) as j:
        beehives_json_dict = json.load(j)

    return beehives_json_dict


def data_from_RESTAPI():
    TABLES_ITS_DATA=sensorNodes_dataDict()
    type_entityid={}
    # print(tuple(TABLES_ITS_DATA.items())[0])
    # print(TABLES_ITS_DATA.items())
    for k, v in TABLES_ITS_DATA.items():
            type_entityid.update(extract_sensor_nodes_meta_data(v))

    return type_entityid


def preparing_beehives_table_data(beehives_json_dict, type_entityid):
    data = []
            
    # beehives_sensornodes=['sensor_node_id', 'bee_hive', 'sensor_node_name', 'sensor_node_type', 
    #                       'sensor_node_entityid', 'time_of_entry']
    # print(json.dumps(type_entityid, indent=4, sort_keys=True))
    for k, v in beehives_json_dict.items():
        each_value = [k, v[0], "LoRa-"+v[1]]
        if each_value[-1] in type_entityid.keys():
            each_value=each_value+type_entityid[each_value[-1]]
        else:
            each_value=each_value+[None, None]
        data.append(each_value)

    return data


def trigger_automatic_db_schema_update(cursor, beehives_json_dict, api_json_dict):
    NEW_SENSOR_NODES=len(list(api_json_dict.keys()))
    NEW_BEEHIVES_JSON_DICT=len(list(beehives_json_dict.keys()))
    # print(len(list(beehives_json_dict.keys())), NEW_BEEHIVES_JSON_DICT)
    # print(len(list(api_json_dict.keys())), NEW_SENSOR_NODES)  # trigger new table creation
    
    query="""SELECT max(sensor_node_id) FROM beehives_sensornodes;"""

    cursor.execute(query)

    CURRENT_TOTAL_SENSOR_NODES=cursor.fetchall()[0][0]
    print("debugging \n")
    print(Total_Sensor_Node_Types)
    if (NEW_SENSOR_NODES>Total_Sensor_Node_Types & NEW_BEEHIVES_JSON_DICT>CURRENT_TOTAL_SENSOR_NODES):
        # --- Trigger the beehives_sensornodes table update
        automatic_update_from_beehives_json(cursor)
        # --- Create new sensornode table, New_Auth_Group Table
        new_sensor_node_starts=Total_Sensor_Node_Types 
        for k, v in list(api_json_dict.items())[new_sensor_node_starts:]:
            cursor.execute(sql_command_from_json(table_name=k, json_data=v))
        # --- Update State Variable
        Total_Sensor_Node_Types=NEW_SENSOR_NODES   # for only during script runtime, currently ambiguous state: 16.07.25
        update_total_sensor_node(Total_Sensor_Node_Types)  # update json file for after new start
        Logger.info(f"new sensor nodes are added to DB, when: {datetime.now().replace(microseconds=0)}")
    else:
        Logger.info(f"currently no new sensor nodes are mounted")

def automatic_update_from_beehives_json(cursor):
    # -- automatic update of the sensor names from json file
    sql = "INSERT INTO beehives_sensornodes (sensor_node_id, bee_hive, sensor_node_name, " \
    "sensor_node_type, sensor_node_entityid, time_of_entry) " \
    "VALUES (%s, %s, %s, %s, %s, NOW())"

    # List of tuples: each tuple is a row to insert
    values = preparing_beehives_table_data(read_beehives_sensornodes_json(), data_from_RESTAPI())

    # Insert multiple rows
    cursor.executemany(sql, values)
    
# --- currently not used, however useful for future implementations
# def filling_sensor_types_upon_condition(cursor):
#     # -- filling sensor node based on sensor name
#     for table_name, type_entityid in extract_sensor_nodes_meta_data().items():
#         cursor.execute(
#             "UPDATE beehives_sensornodes SET sensor_node_type = %s, sensor_node_entityid = %s WHERE sensor_node_name = %s",
#             (type_entityid[0], type_entityid[1], table_name)
#         )


def db_beehives_table_update():
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
    automatic_update_from_beehives_json(cursor)

    # # # --- Filling based on Condition ---
    # use it to triger the table update when New Node is Mounted
    # filling_sensor_types_upon_condition(cursor)

    # # --- Automatic Insertion of New Sensornode Types ---
    # new_sensor_node_insertion()
    # print_db_tables(cursor)
    print_dbTables_Values(cursor)

    conn.commit()
    cursor.close()
    conn.close()

