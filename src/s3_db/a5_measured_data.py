# python 3.12
# sub module of parsing data
# extract, clean, transform into desired data structure


# each sensor data in time_series dict must be assigned to corresponding SQL datatypes supported by PostgreSQL
def extract_sensorsMeasuredData_fromAuthGroupDict(sensor_node_dict:dict) -> list[list, list]:
    """
    params:
        time_series: is from each sensor_node_dict["entities"][0,1,2...]["TIME_SERIES"]
        sensor_node_dict["entities"] is list of dicts-each dict has keys('ENTITY_FIELD', 'SERVER_ATTRIBUTE', 'TIME_SERIES', 'entityId')

    return:
        [["temperature", "pressure"], ["INTEGER", "NUMERIC(10, 2)"]]
    """
    # new_time_series = {key for key in time_series.key()}
    new_time_series = [[], []]
    entities=sensor_node_dict['entities']
    for entity in entities:
        value_tuple = []
        time_series=entity['TIME_SERIES']
        # entityId=entity['entityId']['id']
        # new_time_series[0].append('time_of_save')
        # new_time_series[1].append()
        for k, v in time_series.items():
            if len(new_time_series[0]) < len(time_series.values()):
                new_time_series[0].append(k)
            value=v['value']
            if value.find('.') != -1:
                value_tuple.append(float(value))
            elif value.find("LoRa") != -1:
                value_tuple.append(value)
            else:
                value_tuple.append(int(value))

        # if 'entityId' not in new_time_series[0]:
        #     new_time_series[0].append('entityId')

        # value_tuple.append(entityId)
        new_time_series[1].append(value_tuple)
        value_tuple=None

    return new_time_series

