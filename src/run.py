

import os
import time
import sys
from dotenv import load_dotenv

import __init__
from __init__ import Logger, pkg_path
# from src.s1_db.a99_db_schema_creation import db_schema_creation
# from src.s1_db.a98_db_beehives_update import db_beehives_table_update
# from src.collect.fill import db_communication
from s2_configure.monitor import send_email
from s4_collect.b2_data_collection import beehappy_data_collection

def run_every_5minutes():
    while True:
        try:
            # print("current path::::: ", os.getcwd())
            Logger.info("Starting data collection...")
            beehappy_data_collection()
            Logger.info("Data stored successfully.")

        except Exception as e:
            Logger.exception("Error occurred during data storage and Program Terminated abruptly")
            send_email(
                subject="BeeHappy Data Collection Crashed",
                body=f"An error occurred during data collection and program stopped: {str(e)}",
                to_email="yamini.technical@yahoo.com")
            sys.exit(1) # signal to terminate the program

        else:  # incase no cron job in docker
            time.sleep(300)  # wait exactly 5 minutes

if __name__=="__main__":
    # # Schema creation
    # db_schema_creation()

    # # Table beehive update
    # db_beehives_table_update()

    # # filling values for every 1 minute
    # db_communication()

    # automatic data collection
    run_every_5minutes()
    


