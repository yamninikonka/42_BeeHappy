
import requests
from dotenv import load_dotenv
import os
from pathlib import Path
from json_to_triplequote import extract_sensors_data, automate_table_creation, automatic_d_type, extract_sensor_nodes

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

# Security
load_dotenv() # dotenv_path=Path("../src/data/.env")
api_key = os.getenv("API_KEY")

# Connection to Server using HTTP Request
base_url = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/"

def get_auth_groups_from_url(url):
    r = requests.get(url + api_key)
    auth_groups = r.json()
    return auth_groups


def get_auth_group(group_number: int)->list[str, dict] | None:
    auth_groups = get_auth_groups_from_url(base_url[:-1]+"?x-apikey=")
    match group_number:
        case 1:
            auth_group_name = auth_groups['authGroup'][0]['authGroupName'] #"digital_bee_hive_42-s2120"
        case 2:
            auth_group_name = auth_groups['authGroup'][1]['authGroupName'] #"digital_bee_hive_42_dragino-s31lb"
        case 3:
            auth_group_name = auth_groups['authGroup'][2]['authGroupName'] #"digital_bee_hive_42_dragino-d23-lb"
            
    url = base_url + auth_group_name + "/entityId?page=0&x-apikey=" + api_key
    print(f"{GREEN}-----{auth_group_name}-----{RED}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return [auth_group_name, response.json()]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    
def sql_command_from_json(group:int):
        table_name, json_data = get_auth_group(group)
        each_node_data = extract_sensors_data(json_data)
        time_series = automatic_d_type(tuple(each_node_data.items())[0][1])

        return automate_table_creation(table_name.replace('-', '_'), time_series, foreign_key_ref="beehives_sensornodes")

def all_node_types():
    auth_groups = get_auth_groups_from_url(base_url[:-1]+"?x-apikey=")
    # print(len(auth_groups['authGroup']))
    nodes = {}
    for i in range(1, len(auth_groups['authGroup'])+1):
        # print(extract_sensor_nodes(get_auth_group(i)[1]))
        nodes.update(extract_sensor_nodes(get_auth_group(i)[1]))

    return nodes

# print(all_node_types())
