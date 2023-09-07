import requests
import pandas as pd
import numpy as np
import math
import re

LA_lat = 33.8847
LA_long = -118.4109

def getRelevantBuoys():
    text_data = requests.get('https://www.ndbc.noaa.gov/data/stations/station_table.txt').text
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
    rows.raise_for_status()
    
    # handling data if request is successful
    rows = rows.text.strip().split('\n')
    headers = rows[0].strip().split()
    data = [row.split() for row in rows[1:]]

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
    if deg >= 160 and deg <= 360 and long < 0: 
        return True
    return False


def builddata(df_buoys):
    cols = ['#YY', 'MM', 'DD', 'hh', 'mm', 'WVHT', 'SwH', 'SwP', 'WWH', 'WWP', 'SwD', 'WWD', 'STEEPNESS', 'APD', 'MWD']
    df_main = pd.DataFrame(columns = cols)
    df_main = df_main.rename(columns = {"mm": "minutes"})
    # df_main = pd.DataFrame(columns = df_buoy_data.columns.tolist())
    #for i in range(len(df_buoys)): 
    for i in range(len(df_buoys)):
        lat, long = parse_coordinates(df_buoys.LOCATION.iloc[i])
        angle = calculate_angle((lat, long))
        buoy_id = str(df_buoys.iloc[i, 0])
        if isValidBuoy(angle, long): 
            try: 
                df_main = pd.concat([df_main, getBuoyData(buoy_id)])
                # df_main.append(getBuoyData(buoy_id))
                print(f"got valid data for {buoy_id}")
            except: 
                pass
                # print(f"couldn't get data for buoy {buoy_id}")

    df_main = df_main.rename(columns = {"mm": "minutes"})
    return df_main
