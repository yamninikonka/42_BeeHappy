# python 3.12
# postgresql

import psycopg2.extras
import psycopg2
from datetime import datetime

import __init__
from __init__ import Logger
from s3_db.a1_connect_fetch import sensorNodes_dataDict
from s3_db.a2_parsing_data import sql_command_from_json
from s3_db.a4_meta_data import (extract_sensor_nodes_meta_data)
from s3_db.a5_measured_data import (extract_sensorsMeasuredData_fromAuthGroupDict)
from s3_db.a99_db_schema_creation import (print_dbTables_Values)


def sensor_node_id(cursor, sensor_node_name, sensor_node_type, entityId):
    # -- filling sensor node based on sensor name
    cursor.execute("""
        SELECT sensor_node_id
        FROM beehives_sensornodes
        WHERE sensor_node_type = %s AND sensor_node_name = %s AND sensor_node_entityid = %s""",
        (sensor_node_type, sensor_node_name, entityId)
    )
    id = cursor.fetchone()[0]
    if not id:
        # trigger following actions
        #                           PARENT TABLE
        # 1. read beehives.json file for updates (beehives, sensor node names)
        # 2. insert into table & sensor node type is MISSING
        #                           CHILD TABLE
        # 3. CONDITION upon sensor node name when reading the json from api and parse it
        # 4. INSERT into beehives table and GET the id
        # 5. then FILL child tables
        sql="""
            INSERT INTO beehives_sensornodes (bee_hive, sensor_node_name, sensor_node_type, 
            sensor_node_entityid, time_of_entry) VALUES (%s, %s, %s, %s, NOW())
            """
        values=('-', sensor_node_name, sensor_node_type, entityId)
        cursor.execute_many(sql, values)
        sensor_node_id(cursor, sensor_node_name, sensor_node_type, entityId)
        
    # there is existence of sensor node type in table
    return id


def table_existence_check(cursor, table_name: str, json_data:dict) -> bool:
    # print(table_name)
    query="""
        SELECT EXISTS 
        (SELECT 1 FROM pg_tables
        WHERE schemaname='public' AND tablename=%s)
        """
    cursor.execute(
        query, (table_name,)
    )
    result = cursor.fetchone()[0]
    # ---- Not tested case
    if not result:  # if table does not exist
        cursor.execute(sql_command_from_json(table_name=table_name, json_data=json_data))
        table_existence_check(cursor, table_name, json_data)

    return result


def insert_into_table(cursor, table_name:str, json_data:dict): 
    """
    Table: digital_bee_hive_42_s2120
    Columns: [id, sensor_node_id, time_of_save, lightintensity, raingauge, relativehumidity, temperature, pressure, winddirection, uvindex, windspeed, comments]

    Table: digital_bee_hive_42_dragino_s31lb
    Columns: [id, sensor_node_id, time_of_save, temperature, relativehumidity, comments]

    Table: digital_bee_hive_42_dragino_d23_lb
    Columns: [id, sensor_node_id, time_of_save, tempc3, tempc1, tempc2, comments]
    """
    measured_data=extract_sensorsMeasuredData_fromAuthGroupDict(json_data)
    # ----- column names
    columns='sensor_node_id, time_of_save'
    for each in measured_data[0]:
        columns=columns+', '+each.lower()

    query=f"""INSERT INTO {table_name} ("""+columns+""") VALUES %s"""
    # id, sensor_node_id, time_of_save, sensors[...]

    # ----- handling values
    values=measured_data[1]
    meta_data=extract_sensor_nodes_meta_data(json_data)
    # both are determined from json_data: how many sensor_node_names are there those many measured values
    # i.e; len(values)==len(meta_data)
    for ind in range(len(values)):
        type_and_id=meta_data[list(meta_data.keys())[ind]]
        node_name, node_type, node_id = [list(meta_data.keys())[ind], type_and_id[0], type_and_id[1]]
        sensor_id=sensor_node_id(cursor, node_name, node_type, node_id)
        values[ind]=[sensor_id, datetime.now().replace(microsecond=0)]+values[ind]
    # print(*values, sep="\n")
    psycopg2.extras.execute_values(cursor, query, values)


def filling_tables_with_sensor_measured_values(cursor):
    """
    1. check tables are existed, if not create
    2. fetch sensor_id for child tables
    3. insert data into child tables
    4. 
    """
    # current_time = datetime.now()
    # #------------------------------
    # auth_groups = get_auth_groups_from_url(base_url[:-1]+"?x-apikey=")
    # print(auth_groups)
    # for ind in range(len(auth_groups['authGroup'])):
    #     # 0 - "digital_bee_hive_42-s2120" || 1 - "digital_bee_hive_42_dragino-s31lb" || 2 - "digital_bee_hive_42_dragino-d23-lb"
    #     auth_group_name = auth_groups['authGroup'][ind]['authGroupName']
    #     node_data = get_auth_group(auth_group_name)
    #     # print(node_data[list(node_data.keys())[0]])
    #     # 1. table existence check, if not create and return true
    #     if(table_existence_check(cursor, auth_group_name.replace('-', '_'), ind)):
    #         print(f"{RESET}{table_existence_check(cursor, auth_group_name.replace('-', '_'), ind)}")
    #         # 2. 

    for table_name, json_data in sensorNodes_dataDict().items():
        if table_existence_check(cursor, table_name, json_data):
            insert_into_table(cursor, table_name, json_data)
            Logger.info(f"Inserted data into table: {table_name}")
        else:
            # log error
            # raise Exception(f"{table_name} Table does not exist in DataBase; but it is found in auth_Group_Names from Server API")
            Logger.error(f"{table_name} Table does not exist in DataBase; but it is found in auth_Group_Names from Server API")
    
    print_dbTables_Values(cursor)

# --- Only for testing purpose
# def db_communication():
#     """
#     1. check tables are existed, if not create
#     2. fetch sensor_id for child tables
#     3. insert data into child tables
#     4. 
#     """
#     # Database connection
#     conn = psycopg2.connect(
#                 host="d71a3071-7535-48f1-8b24-d3887122b6a1.postgresql.eu01.onstackit.cloud",
#                 database="beehappydb3",
#                 user="beehappyuser3",
#                 password=db_password,
#                 port="5432"
#             )
#     cursor = conn.cursor()

#     filling_tables_with_sensor_measured_values(cursor)

#     conn.commit()
#     cursor.close()
#     conn.close()



