# python 3.12.10

import requests
import json

api_key = 'X7oqrrCEkOqq2P39MntzXHzopXwo9wMnSW4U03U8SVH4GOsz'

def get_request(url):
    r = requests.get(url + api_key)
    print(r.status_code)

    r_json = r.json()

    print(json.dumps(r_json, indent=4, sort_keys=True))
    print('0'*20, '\n', '-'*20, '\n', '0'*20)
    return r_json

main_page = get_request(url='https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup?x-apikey=')
# Other Sensors
hive1 = get_request(url='https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/'+ main_page['authGroup'][0]['authGroupName']+'/entityId?page=0&x-apikey=')
# Only Relative Humidity and Temperature
hive2 = get_request(url='https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/'+ main_page['authGroup'][1]['authGroupName']+'/entityId?page=0&x-apikey=')
# Temp Sensors
hive3 = get_request(url='https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/'+ main_page['authGroup'][2]['authGroupName']+'/entityId?page=0&x-apikey=')
