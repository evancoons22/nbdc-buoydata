import torch
import pandas as pd
import sqlite3
import numpy as np
import functions

conn = sqlite3.connect('db.db')
data = pd.read_sql_query("SELECT * from main", conn)
# data = functions.cleanData(data)

all_buoys = data[data['buoy_id'] != '46221']
output_buoy = data[data['buoy_id'] == '46221']


data = functions.buildnparray(functions.cleanData(data))
print(data)


# create a new column that days ago from the date of the most recent buoy that is '46221'
use_date = data[data['buoy_id'] == '46221'].iloc[0]['datetime']
data['days_ago'] = data.apply(lambda row: (pd.to_datetime(use_date) - pd.to_datetime(row['datetime'])).days, axis = 1)
