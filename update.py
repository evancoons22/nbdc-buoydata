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
    update_conditions()

# updating buoy data by only replacing dates that haven't been recorded yet 
def update_buoy_data():
    current_date = datetime.now()
    with open('output.txt', 'w') as f: 
        f.write(f"going to update data at {current_date}\n")
        df_buoys = functions.getRelevantBuoys()
    try: 
        for i in range(len(df_buoys)):
            buoy_id = str(df_buoys.iloc[i, 0])

            try:
                df_main = functions.builddata(df_buoys.iloc[i:i+1])
            except: 
                with open('output.txt', 'a') as f:
                    f.write(f"didn't get buoy data from builddata\n")
                continue

            existing_dates = pd.read_sql_query(f"SELECT datetime FROM main WHERE buoy_id = '{buoy_id}'", conn)
            df_main = df_main[~df_main['datetime'].isin(existing_dates['datetime'])]
            df_main.to_sql('main', conn, if_exists='append', index=False)
        with open('output.txt', 'a') as f:
            f.write(f"successfully updated buoy data at {current_date}\n")
    except: 
        with open('output.txt', 'a') as f:
            f.write(f"did not update buoy data at {current_date}\n")
        pass
    # update_conditions()

def update_buoy_data2(): 
    current_date = datetime.now()
    try:
        df_buoys = functions.getRelevantBuoys()
        unique_buoy_ids = pd.read_sql_query("SELECT DISTINCT buoy_id FROM main", conn)
        for buoy_id in unique_buoy_ids['buoy_id']:
            df_main = functions.builddata(df_buoys[df_buoys['buoy_id'] == buoy_id])
            existing_dates = pd.read_sql_query(f"SELECT datetime FROM main WHERE buoy_id = '{buoy_id}'", conn)
            df_main = df_main[~df_main['datetime'].isin(existing_dates['datetime'])]
            df_main.to_sql('main', conn, if_exists='append', index=False)
        with open('output.txt', 'a') as f:
            f.write(f"successfully updated buoy data at {current_date}\n")
    except: 
        with open('output.txt', 'a') as f:
            f.write(f"did not update buoy data at {current_date}\n")
        pass
    


    

schedule.every().day.at("06:00").do(update_buoy_data)
schedule.every().day.at("12:00").do(update_buoy_data)
schedule.every().day.at("18:00").do(update_buoy_data)
schedule.every().day.at("00:00").do(update_buoy_data)

update_buoy_data2()
# Main loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
