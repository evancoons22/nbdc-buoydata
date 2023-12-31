import requests
import pandas as pd
import numpy as np
import math
import re

LA_lat = 33.8847
LA_long = -118.4109


def getRelevantBuoys():
    text_data =  requests.get('https://www.ndbc.noaa.gov/data/stations/station_table.txt').text
    rows = text_data.strip().split('\n')

    # extracting headers
    headers = map(lambda x: x.strip(), rows[0].strip().split('|'))

    # remaining data. (skipping with only `#`)
    data = [row.strip().split('|') for row in rows[2:]]

    df_buoys = pd.DataFrame(data, columns = headers)
    
    # add a column real quick
    df_buoys['angletoLA'] = df_buoys.apply(lambda row: calculate_angle(row.LOCATION), axis = 1)
    return df_buoys



def getBuoyData(buoyid): 
    # Split the text into rows using newline characters
    # trying to get new data
    rows = requests.get(f'https://www.ndbc.noaa.gov/data/realtime2/{buoyid}.spec')
    # handle bad response
    rows.raise_for_status()
    
    # handling data if request is successful
    rows = rows.text.strip().split('\n')
    headers = rows[0].strip().split()
    data = [row.split() for row in rows[2:]]

    df_buoy_data = pd.DataFrame(data, columns=headers)
    return df_buoy_data


def calculate_angle(coords): # (to los angeles)
    buoylat, buoylong = parse_coordinates(coords) if isinstance(coords, str) else coords
    LA_lat = 33.8847
    LA_long = -118.4109
    x = buoylong - LA_long
    y = buoylat - LA_lat
    
    if x >= 0:
        return 90 - math.atan(y / x) * 180 / math.pi 
    elif x < 0: 
        return 270 - math.atan(y / x) * 180 / math.pi
    
    #return math.atan(y / x) * 180 / math.pi
    
    
def parse_coordinates(input_string):
    pattern = r'(\d+\.\d+)\s*([NS])\s*(\d+\.\d+)\s*([EW])'
    match = re.search(pattern, input_string)
    if match:
        latitude = float(match.group(1))
        if match.group(2) == 'S':
            latitude = -latitude
        
        longitude = float(match.group(3))
        if match.group(4) == 'W':
            longitude = -longitude
        
        return latitude, longitude
    else:
        return None
    

def isValidBuoy(deg, long): 
    # print("valid")
    if deg >= 160 and deg <= 360 and long < 0: 
        return True
    return False


def builddata(df_buoys):
    # Convert Year, Month, Day, Hour, minute into one datetime column
       
    cols = ['buoy_id', '#YY', 'MM', 'DD', 'hh', 'mm', 'WVHT', 'SwH', 'SwP', 'WWH', 'WWP', 'SwD', 'WWD', 'STEEPNESS', 'APD', 'MWD']
    df_main = pd.DataFrame(columns = cols)
    for i in range(len(df_buoys)):
        lat, long = parse_coordinates(df_buoys.LOCATION.iloc[i])
        angle = calculate_angle((lat, long))
        buoy_id = str(df_buoys.iloc[i, 0])
        if isValidBuoy(angle, long): 
            try: 
                temp = getBuoyData(buoy_id)
                temp['buoy_id'] = buoy_id
                df_main = pd.concat([df_main, temp])
            except: 
                if len(df_buoys) == 1: 
                    raise ValueError("buoy doesn't exist")
                pass
    # Convert the columns to string type
    df_main[['#YY', 'MM', 'DD', 'hh', 'mm']] = df_main[['#YY', 'MM', 'DD', 'hh', 'mm']].astype(str)
    
    # Add leading zeros to single digit month, day, hour and minute
    df_main['MM'] = df_main['MM'].str.zfill(2)
    df_main['DD'] = df_main['DD'].str.zfill(2)
    df_main['hh'] = df_main['hh'].str.zfill(2)
    df_main['mm'] = df_main['mm'].str.zfill(2)
    
    # Combine the columns to form a datetime string and then convert to datetime
    df_main['datetime'] = pd.to_datetime(df_main['#YY'] + df_main['MM'] + df_main['DD'] + df_main['hh'] + df_main['mm'], format='%Y%m%d%H%M')

    # df_main['datetime'] = pd.to_datetime(df_main[['#YY', 'MM', 'DD', 'hh', 'mm']])
    df_main = df_main.drop(columns=['#YY', 'MM', 'DD', 'hh', 'mm'])

    # df_main = df_main.rename(columns = {"mm": "minutes", "#YY": "Year", "MM":"Month", "DD":"Day"})
    return df_main


def cleanData(data): 
    data = data[['datetime', 'buoy_id', 'WVHT', 'MWD', 'APD']]
    data = data[data['datetime'] > '2023-07-31']
    data = data[data['APD'] != 'MM']
    # just get hourly data, do not worry about minutes
    data['datetime'] = pd.to_datetime(data['datetime'])
    data['datetime'] = data['datetime'].dt.floor('H')

    #convert types of WVHT, MWD, and APD to float
    data['WVHT'] = data['WVHT'].astype(float)
    data['MWD'] = data['MWD'].astype(float)
    data['APD'] = data['APD'].astype(float)
    return data

def buildnparray(data): 
    # the index should be days in datetime days and hours, not every date
    ptable = data.pivot_table(index = 'datetime', columns = 'buoy_id', values = ['WVHT', 'MWD', 'APD'], aggfunc = 'mean')

    ptable = ptable.values
    reshaped_array = ptable.reshape(ptable.shape[0], ptable.shape[1]) 
    # there are 76 buoys
    nbuoys = len(data['buoy_id'].unique())

    # use this for the result
    result = np.array((reshaped_array[:, :nbuoys], reshaped_array[:, nbuoys:nbuoys * 2], reshaped_array[:, nbuoys*2:nbuoys * 3]))

    result = np.transpose(result, (1, 2, 0))

    print(result.shape)

    return result
