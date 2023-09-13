import torch
import pandas as pd
import sqlite3

conn = sqlite3.connect('db.db')
data = pd.read_sql_query("SELECT * from main", conn)

#convert types of WVHT, MWD, and APD to float
data['WVHT'] = data['WVHT'].astype(float)
data['MWD'] = data['MWD'].astype(float)
data['APD'] = data['APD'].astype(float)

# create a new column that days ago from the date of the most recent buoy that is '46221'
use_date = data[data['buoy_id'] == '46221'].iloc[0]['datetime']
data['days_ago'] = data.apply(lambda row: (pd.to_datetime(use_date) - pd.to_datetime(row['datetime'])).days, axis = 1)


# split the data into all buoys, and buoy 46221
all_buoys = data[data['buoy_id'] != '46221']
output_buoy = data[data['buoy_id'] == '46221']

# write a function to create a pytorch tensor from the data. Each row will be a vector. Get the wvht, mwd, and apd from each buoy for 1 day before the date of the most recent buoy 46221
def create_tensor(df):
    # get the rows that are 1 day before the most recent buoy 46221
    df = all_buoys[all_buoys['days_ago'] == 1]
    # get the wvht, mwd, and apd from each buoy
    df = df[['WVHT', 'MWD', 'APD']]
    # convert to a pytorch tensor
    tensor = torch.tensor(df.values)
    return tensor

create_tensor(all_buoys)
