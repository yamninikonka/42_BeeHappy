
import os
import sys
import logging
import json

project_root=os.path.abspath(".")
pkg_path=os.path.abspath(os.path.dirname(__file__))
# print(project_root)
# print(pkg_path)
# print(sys.path)
if not project_root in sys.path:
    sys.path.insert(0, project_root)
    # print(sys.path)

# ----- logging configuration -----
Logger = logging.getLogger(__name__)
logging.basicConfig(filename='src/project/logging.log', encoding='utf-8', level=logging.DEBUG)

# STATE GLOBAL VARIABLES
file="src/data/state_vars.json"
Total_Sensor_Node_Types=0
if os.path.exists(file):
    with open(file) as state_var:
        from_json=json.load(state_var)
        Total_Sensor_Node_Types=from_json["TOTAL_SENSOR_NODE_TYPES"]

else:
    Logger.error(f"{file}: path does not exist. Problem with function:[src/db/a98_db_beehives_update.py/trigger_automatic_db_schema_update]")

Logger.debug(f"TOTAL_SESNOR_NODE_TYPES: {Total_Sensor_Node_Types}")

# --- updating state variable later in program
def update_total_sensor_node(value: int):
    file="src/data/state_vars.json"
    if os.path.exists(file):
        with open(file) as state_var:
            from_json=json.load(state_var)
        
        from_json["TOTAL_SENSOR_NODE_TYPES"]=value
        with open(file, 'w') as state_var:
            json.dump(from_json, state_var)

# tested working as expected, no edge case testing: 16.07.25
# update_total_sensor_node(3)
# print(TOTAL_SENSOR_NODE_TYPES)