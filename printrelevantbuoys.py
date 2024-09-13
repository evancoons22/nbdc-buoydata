import requests
import functions
import pandas as pd
import re

df = functions.getRelevantBuoys()

# buoys that we can pull data from
specbuoys = requests.get('https://www.ndbc.noaa.gov/data/realtime2/')
# use regex to find all the numbers that have the extension .spec
regex = r'([0-9]{5}.spec)'
results = re.findall(regex, specbuoys.text)
# I want the results, but only the numbers, not the .spec
results = [result[:-5] for result in results]

for i in range(len(df)):
    lat, long = functions.parse_coordinates(df.LOCATION.iloc[i])
    if str(df.iloc[i, 0]) in results:
        with open('buoys.txt', 'a') as f:
            f.write("{stationId: '" +  str(df.iloc[i, 0]) + "', name: '" + df.NAME.iloc[i] + "', latitude: " + str(lat) + ", longitude: " + str(long) + "},\n")

# print buoys in this format {name: name, lat: lat, lon: lon, id: id}
