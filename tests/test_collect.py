
import os
import psycopg2
from dotenv import load_dotenv

import __init__
from src.s4_collect.b1_fill_sensor_node_tables import (sensor_node_id, table_existence_check,
                              insert_into_table,
                              sensorNodes_dataDict,
                              extract_sensor_nodes_meta_data)

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


def test_fill_sensor_node_id():
    """
    1. check tables are existed, if not create
    2. fetch sensor_id for child tables
    3. insert data into child tables
    4. 
    """

    for i, json_data in sensorNodes_dataDict().items():
        print(i)
        meta_data=extract_sensor_nodes_meta_data(json_data)
        for k, v in meta_data.items():
            print(k)
            node_name, node_type, node_id = [k, v[0], v[1]]
            sensor_id=sensor_node_id(cursor, node_name, node_type, node_id)
            print(sensor_id, "\n")
        # insert_into_table(cursor, k, v)
    

def test_file_table_existence_check():
    """
    1. check tables are existed, if not create
    2. fetch sensor_id for child tables
    3. insert data into child tables
    4. 
    """

    for i, json_data in sensorNodes_dataDict().items():
        print(i, "                 ", table_existence_check(cursor, i, json_data), "\n")
    # ------- test case for when Table does not exist -------
    # print("new_table", "                 ", table_existence_check(cursor, "new_table", {}), "\n")


def test_fill_insert_into_tables():
    """
    1. check tables are existed, if not create
    2. fetch sensor_id for child tables
    3. insert data into child tables
    4. 
    """

    for k, json_data in sensorNodes_dataDict().items():
        print(k)
        insert_into_table(cursor, k, json_data)
        print("///////////////////////////")

def close_db():
    conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':
    # test_fill_sensor_node_id()
    # test_file_table_existence_check()
    test_fill_insert_into_tables()

    close_db()

