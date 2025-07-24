# python 3.12
# sub module of parsing_data
# extract, clean, transform data into desired SQL format

"""
- sensor_node_type - s2120, d23-lb, s31-lb
- sensor_node_name - "LoRa-2CF7F1C0613005BC", "LoRa-A840411F645AE815", "LoRa-A8404160C85A7A7B"
"""

from typing import Dict



# each sensor data in time_series dict must be assigned to corresponding SQL datatypes supported by PostgreSQL
def timeSeries_dTypeAssignment(time_series:dict) -> list[list, list]:
    """
    params:
        time_series: is from each sensor_node_dict["entity"]["TIME_SERIES"]

    return:
        [["temperature", "pressure"], ["INTEGER", "NUMERIC(10, 2)"]]
    """
    # new_time_series = {key for key in time_series.key()}
    new_time_series = [[], []]
    for k, v in time_series.items():
        new_time_series[0].append(k)
        value = v['value']
        if value.find('.') != -1:
            new_time_series[1].append("NUMERIC(10, 2)")
        elif value.find("LoRa") != -1:
            new_time_series[1].append("VARCHAR(100)")
        else:
            new_time_series[1].append("INTEGER")

    return new_time_series


def tableCreation_SQLStatement(table_name: str, time_series: list[list, list], foreign_key_ref: str):
    """
    params:
        table_name: 
        time_series: returned value from the time_series_d_type_automation()
        foreign_key_ref:
    return:
        triple quote string as representation of sql command to execute
    """
    db_table_start = f"""
                CREATE TABLE IF NOT EXISTS {table_name}(
                    id  SERIAL PRIMARY KEY,
                    sensor_node_id integer,
                    time_of_save timestamp,"""
    sensors = """
                """
    for i, j in zip(*time_series):
        sensors = sensors+f"""    {i} {j},
                """
    #     entityId VARCHAR(100),
    db_table_end = f"""    comments VARCHAR(250),
                    FOREIGN KEY (sensor_node_id) REFERENCES {foreign_key_ref}(sensor_node_id) 
                )
                """
    return db_table_start+sensors+db_table_end

