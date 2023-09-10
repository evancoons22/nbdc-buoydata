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

def update_buoy_data():
    current_date = datetime.now()
    with open('output.txt', 'w') as f: 
        f.write(f"going to update data at {current_date}\n")
    try: 
        df_buoys = functions.getRelevantBuoys()
        df_main = functions.builddata(df_buoys)
        df_main.to_sql('main', conn, if_exists='append', index=False)
        with open('output.txt', 'a') as f:
            f.write(f"successfully updated buoy data at {current_date}\n")
    except: 
        with open('output.txt', 'a') as f:
            f.write(f"did not update buoy data at {current_date}\n")
        pass

    # update_conditions()
    
    # try: 
    #     df_buoys = functions.getRelevantBuoys()
    #     df_main = functions.builddata(df_buoys)
    #     # Get existing data from the database
    #     # df_existing = pd.read_sql_query("SELECT * from main", conn)

    #     # Merge the new data with the existing data
    #     # df_merged = pd.merge(df_main, df_existing, on=['buoy_id', 'date'], how='outer', indicator=True)

    #     # Filter out the rows that exist in both dataframes
    #     # df_main = df_merged[df_merged['_merge'] == 'left_only']
    #     # df_main = df_main.drop(columns=['_merge'])
        
    #     df_main.to_sql('main', conn, if_exists='append', index=False)
    #     print("successfuly udpated buoy data")
    # except: 
    #     print("did not update buoy data")
    #     pass

    # try: 
    #     subprocess.run(['python', 'updateht.py'])
    #     print("updated conditions data")
    # except: 
    #     print("did not update conditions data")
    #     pass


schedule.every().day.at("06:00").do(update_buoy_data)
schedule.every().day.at("12:00").do(update_buoy_data)
schedule.every().day.at("18:00").do(update_buoy_data)
schedule.every().day.at("00:00").do(update_buoy_data)

update_buoy_data()
# Main loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)
