
import os
import json

from __init__ import Logger, pkg_path

# # STATE GLOBAL VARIABLES
# file="src/data/state_vars.json"
# # @TODO: import variable in src/__init__.py
# TotalSensorNodeTypes=0
# if os.path.exists(file):
#     with open(file) as state_var:
#         from_json=json.load(state_var)
#         TotalSensorNodeTypes=from_json["TOTAL_SENSOR_NODE_TYPES"]

# else:
#     Logger.error(f"{file}: path does not exist. Problem with function:[src/db/a98_db_beehives_update.py/trigger_automatic_db_schema_update]")

# Logger.debug(f"TOTAL_SESNOR_NODE_TYPES: {TotalSensorNodeTypes}")


# ----- Function to get the total sensor node types from the state_vars.json file
# tested working as expected, no edge case testing: 16.07.25
file=os.path.join(pkg_path, "s1_data/state_vars.json")
def get_total_sensor_node_types():
    # file=os.path.join(pkg_path, "data/state_vars.json")
    # @TODO: import variable in src/__init__.py
    TotalSensorNodeTypes=0
    if os.path.exists(file):
        with open(file) as state_var:
            from_json=json.load(state_var)
            TotalSensorNodeTypes=from_json["TOTAL_SENSOR_NODE_TYPES"]

    else:
        Logger.error(f"{file}: path does not exist. Problem with function:[src/s2_db/a98_db_beehives_update.py/trigger_automatic_db_schema_update]")

    Logger.debug(f"TOTAL_SESNOR_NODE_TYPES: {TotalSensorNodeTypes}")
    return TotalSensorNodeTypes


# @TODO: import variable in src/__init__.py
# --- updating state variable later in program
def update_total_sensor_node(value: int):
    # file="src/data/state_vars.json"
    if os.path.exists(file):
        with open(file) as state_var:
            from_json=json.load(state_var)
        
        from_json["TOTAL_SENSOR_NODE_TYPES"]=value
        with open(file, 'w') as state_var:
            json.dump(from_json, state_var)

# tested working as expected, no edge case testing: 16.07.25
# update_total_sensor_node(3)
# print(TOTAL_SENSOR_NODE_TYPES)