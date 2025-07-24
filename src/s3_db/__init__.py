# src/s3_db/__init__.py
# -*- coding: utf-8 -*-
# This file is part of the digital beehive project.
# It is subject to the license terms in the LICENSE file found in the top-level directory of this distribution.
"""This module initializes the S3 database package for the digital beehive project.
Currently, it contains commented-out code for global db variables and API json data fetching info for reference."""


# from src.db.a1_connect_fetch import (get_auth_groups_from_url,
#                                   get_table_name_and_its_dict_from_url)

# Connection to Server using HTTP Request
# base_url = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/"

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"
# Global variables for database connection and API data fetching
# AUTH_GROUPS = None  # Will be initialized with auth groups data
# TABLES_ITS_DATA = None  # Will be initialized with table names and their data
# send get request one time to server, multiple requests in different functions 
# can vary the data because of different calls in different times.
# careful about data updation interval for such kind of code implementation
# that is why global variable
# AUTH_GROUPS=get_auth_groups_from_url(base_url[:-1]+"?x-apikey=")
"""
AUTH_GROUPS=
{'authGroup': [{'authGroupName': 'digital_bee_hive_42-s2120', 'authGroupEntityType': 'DEVICE'}, 
{'authGroupName': 'digital_bee_hive_42_dragino-s31lb', 'authGroupEntityType': 'DEVICE'}, 
{'authGroupName': 'digital_bee_hive_42_dragino-d23-lb', 'authGroupEntityType': 'DEVICE'}]}
"""
# print(AUTH_GROUPS)
# TABLES_ITS_DATA=get_table_name_and_its_dict_from_url(AUTH_GROUPS)
"""
TABLES_ITS_DATA=
'digital_bee_hive_42-s2120':
{'entities': [{'entityId': {'entityType': 'DEVICE', 'id': 'cb45a700-fa97-11ef-9d11-f54d6a2753bf'}, 'ENTITY_FIELD': {'name': 'LoRa-2CF7F1C0613005BC', 'type': 'LoRaWAN SenseCAP-S2120'}, 'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 'location': {'ts': 1751716860696, 'value': '42'}, 'devName': {'ts': 0, 'value': ''}, 'longitude': {'ts': 0, 'value': ''}}, 'TIME_SERIES': {'lightIntensity': {'ts': 1751716860360, 'value': '101749'}, 'rainGauge': {'ts': 1751716860360, 'value': '0'}, 'relativeHumidity': {'ts': 1751716860360, 'value': '29'}, 'temperature': {'ts': 1751716860360, 'value': '30.3'}, 'pressure': {'ts': 1751716860360, 'value': '99900'}, 'windDirection': {'ts': 1751716860360, 'value': '0'}, 'uvIndex': {'ts': 1751716860360, 'value': '7.2'}, 'windSpeed': {'ts': 1751716860360, 'value': '0'}}}], 'totalPages': 1, 'totalElements': 1, 'hasNext': False}
-------------------
'digital_bee_hive_42_dragino-s31lb':
{'entities': [{'entityId': {'entityType': 'DEVICE', 'id': 'f99dddb0-ffde-11ef-9545-f1c19ab288c3'}, 'ENTITY_FIELD': {'name': 'LoRa-A840411F645AE815', 'type': 'LoRaWAN Dragino-S31-LB'}, 'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 'location': {'ts': 1751716615412, 'value': '42'}, 'devName': {'ts': 0, 'value': ''}, 'longitude': {'ts': 0, 'value': ''}}, 'TIME_SERIES': {'temperature': {'ts': 1751716615061, 'value': '33.9'}, 'relativeHumidity': {'ts': 1751716615061, 'value': '51.8'}}}, {'entityId': {'entityType': 'DEVICE', 'id': 'a4d4afc0-6eb6-11ef-b667-951a94d6009e'}, 'ENTITY_FIELD': {'name': 'LoRa-A8404138A188669C', 'type': 'LoRaWAN Dragino-S31-LB'}, 'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 'location': {'ts': 1751716655820, 'value': '42'}, 'devName': {'ts': 0, 'value': ''}, 'longitude': {'ts': 0, 'value': ''}}, 'TIME_SERIES': {'temperature': {'ts': 1751716655470, 'value': '34.7'}, 'relativeHumidity': {'ts': 1751716655470, 'value': '45.9'}}}, {'entityId': {'entityType': 'DEVICE', 'id': 'a865a130-ffde-11ef-9545-f1c19ab288c3'}, 'ENTITY_FIELD': {'name': 'LoRa-A84041CC625AE81E', 'type': 'LoRaWAN Dragino-S31-LB'}, 'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 'location': {'ts': 1751716417064, 'value': '42'}, 'devName': {'ts': 0, 'value': ''}, 'longitude': {'ts': 0, 'value': ''}}, 'TIME_SERIES': {'temperature': {'ts': 1751716416694, 'value': '34.1'}, 'relativeHumidity': {'ts': 1751716416694, 'value': '56'}}}], 'totalPages': 1, 'totalElements': 3, 'hasNext': False}
-------------------
'digital_bee_hive_42_dragino-d23-lb':
{'entities': [{'entityId': {'entityType': 'DEVICE', 'id': '6fe2a6f0-2fe0-11f0-ae5e-8797afde61b2'}, 'ENTITY_FIELD': {'name': 'LoRa-A8404160C85A7A7B', 'type': 'LoRaWAN Dragino-D23-LB'}, 'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 'location': {'ts': 1751715820745, 'value': '42'}, 'devName': {'ts': 0, 'value': ''}, 'longitude': {'ts': 0, 'value': ''}}, 'TIME_SERIES': {'tempC3': {'ts': 1751715820386, 'value': '30.5'}, 'tempC1': {'ts': 1751715820386, 'value': '31.8'}, 'tempC2': {'ts': 1751715820386, 'value': '32.9'}}}, {'entityId': {'entityType': 'DEVICE', 'id': '39182140-ffde-11ef-9545-f1c19ab288c3'}, 'ENTITY_FIELD': {'name': 'LoRa-A84041892E5A7A68', 'type': 'LoRaWAN Dragino-D23-LB'}, 'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 'location': {'ts': 1751716105721, 'value': '42'}, 'devName': {'ts': 0, 'value': ''}, 'longitude': {'ts': 0, 'value': ''}}, 'TIME_SERIES': {'tempC3': {'ts': 1751716105353, 
'value': '32.2'}, 'tempC1': {'ts': 1751716105353, 'value': '33'}, 'tempC2': {'ts': 1751716105353, 'value': '32.5'}}}, {'entityId': {'entityType': 'DEVICE', 'id': 'efa9b480-8548-11ee-b88e-89581e0193df'}, 'ENTITY_FIELD': {'name': 'LoRa-A840419521864618', 'type': 'LoRaWAN Dragino-D23-LB'}, 'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 'location': {'ts': 1751716062660, 'value': '42'}, 'devName': {'ts': 0, 'value': ''}, 'longitude': {'ts': 0, 'value': ''}}, 'TIME_SERIES': {'tempC3': {'ts': 1751716062308, 'value': '31.3'}, 'tempC1': {'ts': 1751716062308, 'value': '31.9'}, 'tempC2': {'ts': 1751716062308, 'value': '30.4'}}}], 'totalPages': 1, 'totalElements': 3, 'hasNext': False}
"""

# if __name__=="__main__":
#     for k, v in TABLES_ITS_DATA.items():
#        print(k)
#        print(v)
#        print("-------------------")
   