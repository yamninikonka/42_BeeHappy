

import time
import sys

import __init__
from src import Logger
# from src.s1_db.a99_db_schema_creation import db_schema_creation
# from src.s1_db.a98_db_beehives_update import db_beehives_table_update
# from src.collect.fill import db_communication
from src.automatize import beehappy_data_collection

def run_every_5minutes():
    while True:
        try:
            Logger.info("Starting data collection...")
            beehappy_data_collection()
            Logger.info("Data stored successfully.")
            # time.sleep(300)  # wait exactly 5 minute
        except Exception as e:
            Logger.exception("Error occurred during data storage and Program Terminated abruptly")
            sys.exit(1) # signal to terminate the program
        else:  # incase no cron job in docker
            time.sleep(300)  # wait exactly 5 minute


if __name__=="__main__":
    # # Schema creation
    # db_schema_creation()

    # # Table beehive update
    # db_beehives_table_update()

    # # filling values for every 1 minute
    # db_communication()

    # automatic data collection
    run_every_5minutes()
    


