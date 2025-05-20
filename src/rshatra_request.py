
import requests
import psycopg2
from dotenv import load_dotenv
import os
from datetime import datetime

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

load_dotenv()
api_key = os.getenv("API_KEY")
db_password = os.getenv("DB_PASSWORD")


# Database connection
conn = psycopg2.connect(
    host="myapm.eu",
    database="bee_happy_db",
    user="bee_happy_user",
    password=db_password,
    port="5432"
)
cursor = conn.cursor()

current_time = datetime.now()


base_url = "https://apis.smartcity.hn/bildungscampus/iotplatform/digitalbeehive/v1/authGroup/"

def get_auth_group(group_number):
    match group_number:
        case 1:
            auth_group_name = "digital_bee_hive_42-s2120"
        case 2:
            auth_group_name = "digital_bee_hive_42_dragino-s31lb"
        case 3:
            auth_group_name = "digital_bee_hive_42_dragino-d23-lb"
            
    url = base_url + auth_group_name + "/entityId?page=0&x-apikey=" + api_key
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None
    

date_json1 = get_auth_group(1)
if date_json1:
    entities = date_json1.get("entities", [])
    for entity in entities:
        temperature = entity.get("TIME_SERIES", {}).get("temperature", {}).get("value", "N/A")
        lightIntensity = entity.get("TIME_SERIES", {}).get("lightIntensity", {}).get("value", "N/A")
        rainGauge = entity.get("TIME_SERIES", {}).get("rainGauge", {}).get("value", "N/A")
        relativeHumidity = entity.get("TIME_SERIES", {}).get("relativeHumidity", {}).get("value", "N/A")
        pressure = entity.get("TIME_SERIES", {}).get("pressure", {}).get("value", "N/A")
        windDirection = entity.get("TIME_SERIES", {}).get("windDirection", {}).get("value", "N/A")
        uvIndex = entity.get("TIME_SERIES", {}).get("uvIndex", {}).get("value", "N/A")
        windSpeed = entity.get("TIME_SERIES", {}).get("windSpeed", {}).get("value", "N/A")
        
        print(f"{GREEN}Temperature:{RESET} {RED}{temperature}{RESET}")
        print(f"{GREEN}Light Intensity:{RESET} {RED}{lightIntensity}{RESET}")
        print(f"{GREEN}Rain Gauge:{RESET} {RED}{rainGauge}{RESET}")
        print(f"{GREEN}Relative Humidity:{RESET} {RED}{relativeHumidity}{RESET}")
        print(f"{GREEN}Pressure:{RESET} {RED}{pressure}{RESET}")
        print(f"{GREEN}Wind Direction:{RESET} {RED}{windDirection}{RESET}")
        print(f"{GREEN}UV Index:{RESET} {RED}{uvIndex}{RESET}")
        print(f"{GREEN}Wind Speed:{RESET} {RED}{windSpeed}{RESET}")
        #cursor.execute("""
                       #INSERT INTO tempreture (time, value) VALUES (%s, %s)
                       #""", (current_time, temperature))

        
    print("\n")

date_json2 = get_auth_group(2)
if date_json2:
    entities = date_json2.get("entities", [])
    
    for entity in entities:
        entity_id = entity.get("entityId", {}).get("id", "N/A")
        name = entity.get("ENTITY_FIELD", {}).get("name", "N/A")
        temperature = entity.get("TIME_SERIES", {}).get("temperature", {}).get("value", "N/A")
        relativeHumidity = entity.get("TIME_SERIES", {}).get("relativeHumidity", {}).get("value", "N/A")
        print(f"From Entity {name}, ID: {entity_id} we got the following data:")
        print(f"{GREEN}Temperature:{RESET} {RED}{temperature}{RESET}, {GREEN}Relative Humidity:{RESET} {RED}{relativeHumidity}{RESET}")
        
    print("\n")

date_json = get_auth_group(3)
if date_json:
    entities = date_json.get("entities", [])
    
    for entity in entities:
        entity_id = entity.get("entityId", {}).get("id", "N/A")
        name = entity.get("ENTITY_FIELD", {}).get("name", "N/A")
        temp1 = entity.get("TIME_SERIES", {}).get("tempC1", {}).get("value", "N/A")
        temp2 = entity.get("TIME_SERIES", {}).get("tempC2", {}).get("value", "N/A")
        temp3 = entity.get("TIME_SERIES", {}).get("tempC3", {}).get("value", "N/A")
        print(f"From Entity {name}, ID: {entity_id} we got the following data:")
        print(f"{GREEN}Temperature 1:{RESET} {RED}{temp1}{RESET}, {GREEN}Temperature 2:{RESET} {RED}{temp2}{RESET}, {GREEN}Temperature 3:{RESET} {RED}{temp3}{RESET}")
        
    print("\n")

    cursor.execute(
        """
        SELECT * FROM measuring_stations;
        """
    )

conn.commit()
cursor.close()
conn.close()
