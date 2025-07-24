
import __init__
from src.s3_db.a1_connect_fetch import (get_authGroups_fromUrl,
                                     get_tableName_and_itsDict_fromUrl) 
from src.s3_db.a2_parsing_data import (sql_command_from_json)
from src.s3_db.a3_json_to_triplequote import (timeSeries_dTypeAssignment,
                                           tableCreation_SQLStatement)
from src.s3_db.a4_meta_data import(extract_sensors_timeSeriesData,
                                extract_sensor_nodes_meta_data)
from src.s3_db.a5_measured_data import (extract_sensorsMeasuredData_fromAuthGroupDict)

base_url = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/"

AUTH_GROUPS=get_authGroups_fromUrl(base_url[:-1]+"?x-apikey=")
TABLES_ITS_DATA=get_tableName_and_itsDict_fromUrl(AUTH_GROUPS)

def test_connect_fetch():
    
    for each in AUTH_GROUPS["authGroup"]:
        print(each, "\n----------------\n")

    for k, v in TABLES_ITS_DATA.items():
       print(k)
       print(v)
       print("+++++++++++++++++++++")

    print("----------------------")

def test_parsing_data_sql():
    for k, v in TABLES_ITS_DATA.items():
        print(sql_command_from_json(k, v))
        print("+++++++++++++++++++++++")

def test_json_to_triplequote_timeSeries_dTypeAssignment():
    for k, v in TABLES_ITS_DATA.items():
        each_node_data=extract_sensors_timeSeriesData(v)
        print(timeSeries_dTypeAssignment(tuple(each_node_data.items())[0][1]))
        print(".......................")

def test_json_to_triplequote_tableCreation_SQLStatement():
    for k, v in TABLES_ITS_DATA.items():
        each_node_data=extract_sensors_timeSeriesData(v)
        table=tableCreation_SQLStatement(k, 
                                       timeSeries_dTypeAssignment(tuple(each_node_data.items())[0][1]), 
                                       foreign_key_ref="beehives_sensornodes")
        # print(table)
        print(table)
        print("------------------------")

def test_meta_data_extract_sensors_timeSeriesData():
    for k, v in TABLES_ITS_DATA.items():
        node=extract_sensors_timeSeriesData(v)
        print(node)
        print("+++++++++++++++++++++++")

def test_meta_data_extract_sensor_nodes_meta_data():
    for k, v in TABLES_ITS_DATA.items():
        nodes=extract_sensor_nodes_meta_data(v)
        print(nodes)
        print("+++++++++++++++++++++++")

def test_measured_data_extract_sensorsMeasuredData_fromAuthGroupDict():
    for k, v in TABLES_ITS_DATA.items():
        # each_node_data=extract_sensors_time_series_data(v)
        measured_data=extract_sensorsMeasuredData_fromAuthGroupDict(sensor_node_dict=v)
        print(measured_data)
        print("************************")

if __name__=="__main__":
    
    # test_connect_fetch()

    # test_parsing_data_sql()

    # test_json_to_triplequote_timeSeries_dTypeAssignment()
    # test_json_to_triplequote_tableCreation_SQLStatement()

    # test_meta_data_extract_sensors_timeSeriesData()
    test_meta_data_extract_sensor_nodes_meta_data()

    test_measured_data_extract_sensorsMeasuredData_fromAuthGroupDict()
    pass
