import torch
import pandas as pd
import sqlite3
import numpy as np

conn = sqlite3.connect('db.db')
data = pd.read_sql_query("SELECT * from main", conn)
# delete all columns except for datetime, buoy_id, WVHT, MWD, and apd
data = data[['datetime', 'buoy_id', 'WVHT', 'MWD', 'APD']]

# just get hourly data, do not worry about minutes
data['datetime'] = pd.to_datetime(data['datetime'])
data['datetime'] = data['datetime'].dt.floor('H')

# selecet data that is only after 7/31/2023
data = data[data['datetime'] > '2023-07-31']

# for each unique buoy_id, create a numbered mapping
buoy_ids = data['buoy_id'].unique()
map = {}
for (k, v) in enumerate(buoy_ids): 
    map[v] = k


# delete rows where data['APD'] == 'MM'
data = data[data['APD'] != 'MM']

# format data to display in days and hours

#convert types of WVHT, MWD, and APD to float
data['WVHT'] = data['WVHT'].astype(float)
data['MWD'] = data['MWD'].astype(float)
data['APD'] = data['APD'].astype(float)

# the index should be days in datetime days and hours, not every date
ptable = data.pivot_table(index = 'datetime', columns = 'buoy_id', values = ['WVHT', 'MWD', 'APD'], aggfunc = 'mean')
# ptable = data.pivot_table(index = 'datetime', columns = ['WVHT', 'MWD', 'APD'], values = 'buoy_id', aggfunc = 'mean')
# print(ptable)


# read sql data into numpy array
ptable = ptable.values
reshaped_array = ptable.reshape(ptable.shape[0], ptable.shape[1]) 
# using reshaped array, split into 3 arrays, one for column 0 to 76, then 76 to 152, then 152 to 228, concatenate them so the resulting shape is (1099, 76, 3)
reshaped_array = np.array((reshaped_array[:, :76], reshaped_array[:, 76:152], reshaped_array[:, 152:228]))

nbuoys = data['buoy_id'].unique()
# reshaped_array =[reshaped_array[:][:nbuoys], reshaped_array[:][nbuoys:nbuoys + nbuoys], reshaped_array[:][nbuoys:]]

print(reshaped_array.shape)
print(reshaped_array)


# print(data)

# create a new column that days ago from the date of the most recent buoy that is '46221'
use_date = data[data['buoy_id'] == '46221'].iloc[0]['datetime']
data['days_ago'] = data.apply(lambda row: (pd.to_datetime(use_date) - pd.to_datetime(row['datetime'])).days, axis = 1)


# split the data into all buoys, and buoy 46221
all_buoys = data[data['buoy_id'] != '46221']
output_buoy = data[data['buoy_id'] == '46221']

