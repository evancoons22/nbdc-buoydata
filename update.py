from datetime import datetime, timedelta
import schedule
import pandas as pd
import numpy as np
import sqlite3
import time
import subprocess

import functions


conn = sqlite3.connect('db.db')
# df_main.to_sql('main', conn, if_exists='replace', index=False)


def update_conditions(): 
    try: 
        subprocess.run(['python', 'updateht.py'])
        with open('output.txt', 'a') as f:
            f.write("updated conditions data\n")
    except: 
        with open('output.txt', 'a') as f:
            f.write("did not update conditions data\n")
        pass

def init_buoy_data():
    current_date = datetime.now()
    with open('output.txt', 'w') as f: 
        f.write(f"going to init data at {current_date}\n")
    try: 
        df_buoys = functions.getRelevantBuoys()
        df_main = functions.builddata(df_buoys)
        df_main.to_sql('main', conn, if_exists='append', index=False)
        with open('output.txt', 'a') as f:
            f.write(f"successfully init buoy data at {current_date}\n")
    except: 
        with open('output.txt', 'a') as f:
            f.write(f"did not init buoy data at {current_date}\n")
        pass

# updating buoy data by only replacing dates that haven't been recorded yet 
def update_buoy_data(): 
    try:
        current_date = datetime.now()
        df_buoys = functions.getRelevantBuoys()
        df_buoys = df_buoys.rename(columns = {"# STATION_ID": "buoy_id"})

        unique_buoy_ids = pd.read_sql_query("SELECT DISTINCT buoy_id FROM main", conn)

        n = 0

        for buoy_id in unique_buoy_ids['buoy_id']:
            df_main = functions.builddata(df_buoys[df_buoys['buoy_id'] == buoy_id])
            existing_dates = pd.read_sql_query(f"SELECT datetime FROM main WHERE buoy_id = '{buoy_id}'", conn)
            df_main = df_main[~df_main['datetime'].isin(existing_dates['datetime'])]
            df_main.to_sql('main', conn, if_exists='append', index=False)
            n += len(df_main)
        # writing to output to update
        with open('output.txt', 'a') as f:
            f.write(f"successfully updated buoy data at {current_date}\n")
            f.write(f"with {n} rows\n")
    except: 
        with open('output.txt', 'a') as f: 
            f.write("failed to update data\n")

    update_conditions()

schedule.every().day.at("06:00").do(update_buoy_data)
schedule.every().day.at("12:00").do(update_buoy_data)
schedule.every().day.at("18:00").do(update_buoy_data)
schedule.every().day.at("00:00").do(update_buoy_data)

# update_buoy_data()
# Main loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(120)
