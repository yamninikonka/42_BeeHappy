

from typing import Dict

from s3_db.a3_json_to_triplequote import (tableCreation_SQLStatement,
                                           timeSeries_dTypeAssignment)
from s3_db.a4_meta_data import (extract_sensors_timeSeriesData)
# from s3_db.a5_measured_data import (extract_sensorsMeasuredData_fromAuthGroupDict)


    
def sql_command_from_json(table_name: str, json_data: Dict):
        # table_name, json_data = get_auth_group(group)
        each_node_data = extract_sensors_timeSeriesData(json_data)
        time_series = timeSeries_dTypeAssignment(tuple(each_node_data.items())[0][1])

        return tableCreation_SQLStatement(table_name,   #table_name.replace('-', '_')
                                            time_series, foreign_key_ref="beehives_sensornodes")


# if __name__=="__main__":
#     data=extract_sensors_data_from_API(get_auth_group(0)[1])
#     print(data)
#     data=extract_sensors_data_from_API(get_auth_group(1)[1])
#     print(data)
#     data=extract_sensors_data_from_API(get_auth_group(2)[1])
#     print(data)
