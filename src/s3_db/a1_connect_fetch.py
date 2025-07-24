# python 3.12
# postgreSQL
# connect to server and send http GET request. 
# once connection is established, then fetch the data, finally store it local variable for further processing

import requests
from pathlib import Path

from __init__ import Logger
from s2_configure.db import base_url, api_key


# first page in an server to know which sensor node types are mounted
# s2120, s31lb, d23-lb
def get_authGroups_fromUrl(url):
    r = requests.get(url + api_key)
    auth_groups = r.json()
    return auth_groups

# each sensor node(auth group) dict | keys: entities, hasNext, totalElements, totalPages
def get_tableName_and_itsDict_fromUrl(auth_groups: dict)->list[str, dict] | None:
    """
    return: ["digital_bee_hive_42-s2120", {'entities', 'totalpages', 'hasNext', ''}]
    """
    # auth_groups = get_auth_groups_from_url(base_url[:-1]+"?x-apikey=") - @old implementation
    groups_corresponding_dict={}
    for ind in range(len(auth_groups['authGroup'])):
        # ind = 0 - "digital_bee_hive_42-s2120"
        # ind = 1 - "digital_bee_hive_42_dragino-s31lb"
        # ind = 2 - "digital_bee_hive_42_dragino-d23-lb"
        auth_group_name = auth_groups['authGroup'][ind]['authGroupName']
            
        url = base_url + auth_group_name + "/entityId?page=0&x-apikey=" + api_key
        # print(f"{GREEN}-----{ind} {auth_group_name}-----{RED}")
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for bad responses
            groups_corresponding_dict[auth_group_name.replace('-', '_')]=response.json()
            # return [auth_group_name, response.json()]
        except requests.exceptions.RequestException as e:
            # print(f"An error occurred: {e}")
            Logger.error(f"An error occurred during request hadling: {e}")
            return None
        except ValueError as e:
            # print(f"Error parsing JSON response: {e}")
            Logger.error(f"Error parsing JSON response: {e}")
            return None
        # else:
    return groups_corresponding_dict
    
def sensorNodes_dataDict():
    AUTH_GROUPS=get_authGroups_fromUrl(base_url[:-1]+"?x-apikey=")
    TABLES_ITS_DATA=get_tableName_and_itsDict_fromUrl(AUTH_GROUPS)
    if TABLES_ITS_DATA:
        return TABLES_ITS_DATA
    else:
        raise ValueError(f"TABELS_ITS_DATA is NONE")
    
# def auth_group_dict_for_local_processing():
#     group_dict={}
#     for ind in range(len(AUTH_GROUP['entities']))
#         info=get_auth_group(group_number=ind)

# if __name__=="__main__":
#     AUTH_GROUPS=get_auth_groups_from_url(base_url)
#     print(AUTH_GROUPS)