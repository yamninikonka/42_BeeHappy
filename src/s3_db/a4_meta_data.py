# python 3.12
# sub module for parsing data
# db schema creation & meta data extraction, cleaning & transformation

from typing import Dict

# from s3_db import RED, GREEN, RESET


def extract_sensors_timeSeriesData(json_data: dict)->Dict[str, Dict[str, str]]:
    """"
    params:
        json_data: each sensor_node_type(s2120, d23-lb, s31-lb) is an single page.
        that is read from an http get request and parsed then pass it as an argument to this function
        e.g: json_data = {'entities': 
                            [{'entityId': {'entityType': 'DEVICE', 'id': 'cb45a700-fa97-11ef-9d11-f54d6a2753bf'}, 
                              'ENTITY_FIELD': {'name': 'LoRa-2CF7F1C0613005BC', 'type': 'LoRaWAN SenseCAP-S2120'}, 
                              'SERVER_ATTRIBUTE': {'latitude': {'ts': 0, 'value': ''}, 
                                                   'location': {'ts': 1751716860696, 'value': '42'}, 
                                                   'devName': {'ts': 0, 'value': ''}, 
                                                   'longitude': {'ts': 0, 'value': ''}}, 
                              'TIME_SERIES': {'lightIntensity': {'ts': 1751716860360, 'value': '101749'}, 
                                              'rainGauge': {'ts': 1751716860360, 'value': '0'}, 
                                              'relativeHumidity': {'ts': 1751716860360, 'value': '29'}, 
                                              'temperature': {'ts': 1751716860360, 'value': '30.3'}, 
                                              'pressure': {'ts': 1751716860360, 'value': '99900'}, 
                                              'windDirection': {'ts': 1751716860360, 'value': '0'}, 
                                              'uvIndex': {'ts': 1751716860360, 'value': '7.2'}, 
                                              'windSpeed': {'ts': 1751716860360, 'value': '0'}
                                              }
                            }], 
                          'totalPages': 1, 
                          'totalElements': 1, 
                          'hasNext': False}
    
    return:
        timeseries data of each entity in an page(sensor_node_type)
    """
    if json_data:
        entities = json_data.get("entities", [])
        each_node_time_series = {}
        for entity in entities:
        #     print(f"{RESET}{entity["entityId"]["id"]}")
        #     print(f"{RED}{entity["ENTITY_FIELD"]["name"]}, ---, {entity["ENTITY_FIELD"]["type"]}")
        #     print(f"{GREEN}{dict(entity["TIME_SERIES"].items())}")
            each_node_time_series[entity["ENTITY_FIELD"]["name"]] = dict(entity["TIME_SERIES"].items())

        # print("\n=======================================================================\n")

        return each_node_time_series
    else:
         raise ValueError("Json Data is None")
    

# extracts, node_name, node_type, entity_id
def extract_sensor_nodes_meta_data(json_data: dict)->Dict[str, Dict[str, str]]:
    """"
    params:
        json_data: each sensor_node_type(s2120, d23-lb, s31-lb) is an single page.
        that is read from an http get request and parsed then pass it as an argument to this function
    
    return:
        timeseries data of each entity in an page(sensor_node_type)
    """
    if json_data:
        entities = json_data.get("entities", [])
        each_node_types = {}
        for entity in entities:
            each_node_types[entity["ENTITY_FIELD"]["name"]] = [entity["ENTITY_FIELD"]["type"], entity['entityId']['id']]

        # print("\n=======================================================================\n")

    return each_node_types

