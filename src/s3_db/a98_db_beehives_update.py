# python 3.11
# postgre db
"""
* This module is responsible for updating only the beehives_sensornodes table in the database.
* It reads the beehives_sensornodes.json file and updates the database accordingly.
* It also checks for the new sensor nodes mounted in future and triggers the automatic update of the database schema
and the beehives_sensornodes table.
"""

import psycopg2
import dotenv 
import os
import json
from datetime import datetime

from __init__ import Logger, pkg_path
from s2_configure.config import (update_total_sensor_node, get_total_sensor_node_types)
from s3_db.a1_connect_fetch import (sensorNodes_dataDict)
from s3_db.a2_parsing_data import (sql_command_from_json)
from s3_db.a4_meta_data import (extract_sensor_nodes_meta_data)
from utils.db import (print_dbTables_Columns, print_dbTables_Values)


# argument/parameter of preparing_beehives_table_data
def read_beehives_sensornodes_json(j_file=os.path.join(pkg_path, "s1_data/beehives_sensors_v2.json")):
    with open(j_file) as j:
        beehives_json_dict = json.load(j)

    return beehives_json_dict

# argument/parameter of preparing_beehives_table_data
def data_from_RESTAPI():
    TABLES_ITS_DATA=sensorNodes_dataDict()
    type_entityid={}
    # print(tuple(TABLES_ITS_DATA.items())[0])
    # print(TABLES_ITS_DATA.items())
    for k, v in TABLES_ITS_DATA.items():
            type_entityid.update(extract_sensor_nodes_meta_data(v))

    return type_entityid

# helper function of automatic_update_from_beehives_json
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

# in future any sensor node updates should trigger the whole db schema update, that can be achieved with below function
def trigger_automatic_db_schema_update(cursor, beehives_json_dict, api_json_dict):
    NEW_SENSOR_NODES=len(list(api_json_dict.keys()))
    NEW_BEEHIVES_JSON_DICT=len(list(beehives_json_dict.keys()))
    # print(len(list(beehives_json_dict.keys())), NEW_BEEHIVES_JSON_DICT)
    # print(len(list(api_json_dict.keys())), NEW_SENSOR_NODES)  # trigger new table creation
    
    query="""SELECT max(sensor_node_id) FROM beehives_sensornodes;"""
    cursor.execute(query)

    CURRENT_TOTAL_SENSOR_NODES=cursor.fetchall()[0][0]
    TotalSensorNodeTypes=get_total_sensor_node_types()

    # If the new sensor node is mounted and beehives json file must be updated, if it is not: no update
    if (NEW_SENSOR_NODES>TotalSensorNodeTypes & NEW_BEEHIVES_JSON_DICT>CURRENT_TOTAL_SENSOR_NODES):
        # --- 1. Trigger the beehives_sensornodes table update
        automatic_update_from_beehives_json(cursor)

        # --- 2. Create new sensornode table, New_Auth_Group Table
        new_sensor_node_starts=TotalSensorNodeTypes 
        for k, v in list(api_json_dict.items())[new_sensor_node_starts:]:
            cursor.execute(sql_command_from_json(table_name=k, json_data=v))

        # --- 3. Update State Variable
        TotalSensorNodeTypes=NEW_SENSOR_NODES   # for only during script runtime, currently ambiguous state: 16.07.25
        update_total_sensor_node(TotalSensorNodeTypes)  # update json file for after new start

        Logger.info(f"new sensor nodes are added to DB, when: {datetime.now().replace(microseconds=0)}")
    else:
        Logger.info(f"currently no new sensor nodes are mounted")

# when all sensor node column values are in hand then below function fills the beehives_sensornodes table
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


def db_beehives_table_update(cursor):
    
    # -------------- Filling Database Table -------------------
    # # --- 1. Beehives_Sensornodes Filling Values ---
    automatic_update_from_beehives_json(cursor)

    # # # --- 2. Filling based on Condition ---
    # use it to triger the table update when New Node is Mounted
    # filling_sensor_types_upon_condition(cursor)

    # # --- 3. Automatic Insertion of New Sensornode Types ---
    # new_sensor_node_insertion()
    # print_db_tables(cursor)
    print_dbTables_Values(cursor)


