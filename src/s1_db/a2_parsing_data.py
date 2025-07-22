
from typing import Dict
import requests
from dotenv import load_dotenv
import os
from pathlib import Path
from src.s1_db.a3_json_to_triplequote import (tableCreation_SQLStatement,
                                           timeSeries_dTypeAssignment)
from src.s1_db.a4_meta_data import (extract_sensors_timeSeriesData,
                                 extract_sensor_nodes_meta_data)
from src.s1_db.a5_measured_data import (extract_sensorsMeasuredData_fromAuthGroupDict)


GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# # Security
# load_dotenv() # dotenv_path=Path("../src/data/.env")
# api_key = os.getenv("API_KEY")

# # Connection to Server using HTTP Request
# base_url = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/"

# # first page in an server to know which sensor node types are mounted
# # s2120, s31lb, d23-lb
# def get_auth_groups_from_url(url):
#     r = requests.get(url + api_key)
#     auth_groups = r.json()
#     return auth_groups

# # each sensor node dict | keys: entities, hasNext, totalElements, totalPages
# def get_auth_group(group_number: int)->list[str, dict] | None:
#     auth_groups = get_auth_groups_from_url(base_url[:-1]+"?x-apikey=")
#     for ind in range(len(auth_groups['authGroup'])):
#         # 0 - "digital_bee_hive_42-s2120"
#         # 1 - "digital_bee_hive_42_dragino-s31lb"
#         # 2 - "digital_bee_hive_42_dragino-d23-lb"
#         if ind+1==group_number:
#             auth_group_name = auth_groups['authGroup'][ind]['authGroupName']
            
#     url = base_url + auth_group_name + "/entityId?page=0&x-apikey=" + api_key
#     print(f"{GREEN}-----{auth_group_name}-----{RED}")
#     try:
#         response = requests.get(url)
#         response.raise_for_status()  # Raise an error for bad responses
#         return [auth_group_name, response.json()]
#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred: {e}")
#         return None
#     except ValueError as e:
#         print(f"Error parsing JSON response: {e}")
#         return None
    
# def auth_group_dict_for_local_processing():
#     group_dict={}
#     for ind in range(len(AUTH_GROUP['entities']))
#         info=get_auth_group(group_number=ind)
    
def sql_command_from_json(table_name: str, json_data: Dict):
        # table_name, json_data = get_auth_group(group)
        each_node_data = extract_sensors_timeSeriesData(json_data)
        time_series = timeSeries_dTypeAssignment(tuple(each_node_data.items())[0][1])

        return tableCreation_SQLStatement(table_name,   #table_name.replace('-', '_')
                                            time_series, foreign_key_ref="beehives_sensornodes")

# EQUIVALENT TO GLOBAL VARIABLE "TABLES_ITS_DATA"
# -----------------------------------------------
# def all_node_types_from_restAPI(auth_groups):
#     # auth_groups = get_auth_groups_from_url(base_url[:-1]+"?x-apikey=")
#     # print(len(auth_groups['authGroup']))
#     nodes = {}
#     for i in range(1, len(auth_groups['authGroup'])+1):
#         # print(extract_sensor_nodes(get_auth_group(i)[1]))
#         nodes.update(extract_sensor_nodes_meta_data(get_auth_group(i)[1]))

#     return nodes

# print(all_node_types())


# if __name__=="__main__":
#     data=extract_sensors_data_from_API(get_auth_group(0)[1])
#     print(data)
#     data=extract_sensors_data_from_API(get_auth_group(1)[1])
#     print(data)
#     data=extract_sensors_data_from_API(get_auth_group(2)[1])
#     print(data)
