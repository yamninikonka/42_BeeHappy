

from db.parsing_data import get_auth_group
from db.json_to_triplequote import extract_sensors_time_series_data, automatic_table_creation, time_series_d_type_automation

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def test_extraction(group:int):
        table_name, json_data = get_auth_group(group)
        each_node_data = extract_sensors_time_series_data(json_data)
        print(each_node_data)
        # -- SINGLE VALUE
        print(f"{RESET}{tuple(each_node_data.items())[0][1]}")
        # -- ALL VALUES
        # for each_sensor in tuple(each_node_data_2.items()):
        #     print(f"{RESET}{each_sensor[1]}")

def test_d_type(group:int):
        table_name, json_data = get_auth_group(group)
        each_node_data = extract_sensors_time_series_data(json_data)
        print(time_series_d_type_automation(tuple(each_node_data.items())[0][1]))
        # for i, j in zip(*automatic_d_type(tuple(each_node_data.items())[0][1])):
        #     print(i, j)

def test_sql_command(group:int):
        table_name, json_data = get_auth_group(group)
        each_node_data = extract_sensors_time_series_data(json_data)
        time_series = time_series_d_type_automation(tuple(each_node_data.items())[0][1])

        print(time_series)
        print(f"{GREEN}{automatic_table_creation(table_name, time_series, foreign_key_ref="beehives_sensornodes")}")

if __name__ == "__main__":
    # extract_sensors_data(get_auth_group(1)[1])
    # extract_sensors_data(get_auth_group(2)[1])
    # extract_sensors_data(get_auth_group(3)[1])

    # # ----- testing extract_sensors_data -----
    # # = authgroup 1
    # test_extraction(1)
    # # = authgroup 2
    # test_extraction(2)
    # # = authgroup 3
    # test_extraction(3)
    # # ------------------------ END ---------------------------

    # # ----- dtype conversion -----
    # # = authgroup 1
    # test_d_type(1)
    # # = authgroup 2
    # test_d_type(2)
    # # = authgroup 3
    # test_d_type(3)

    # ----- table creation -----
    # = authgroup 1
    test_sql_command(1)
    # = authgroup 1
    test_sql_command(2)
    # = authgroup 1
    test_sql_command(3)
    pass
