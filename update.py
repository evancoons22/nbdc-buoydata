import requests
from datetime import datetime, timedelta
import schedule
import pandas as pd
import numpy as np
import math
import re
import sqlite3
import time

import functions


conn = sqlite3.connect('db.db')
# df_main.to_sql('main', conn, if_exists='replace', index=False)
df_buoys = functions.getRelevantBuoys()


def update_data():
    print("the data is being updated")
    df_buoys = functions.getRelevantBuoys()
    df_main = functions.build_data(df_buoys)
    df_main.to_sql('main', conn, if_exists='append', index=False)
    print("successfuly udpated data")

    # Get current date and time
    now = datetime.now()
    # Calculate the date 5 days ago
    five_days_ago = now - timedelta(days=5)

    # Convert the date to the format used in the dataframe
    year = five_days_ago.year
    month = five_days_ago.month
    day = five_days_ago.day

    # Delete rows older than 5 days
    query = f"DELETE FROM main WHERE #YY < {year} OR (MM < {month} AND #YY = {year}) OR (DD < {day} AND MM = {month} AND #YY = {year})"
    conn.execute(query)
    conn.commit()

schedule.every().day.at("06:00").do(update_data)
schedule.every().day.at("12:00").do(update_data)
schedule.every().day.at("18:00").do(update_data)
schedule.every().day.at("00:00").do(update_data)



# Main loop to keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)