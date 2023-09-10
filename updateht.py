import subprocess
import sqlite3
import time
from datetime import datetime

# Run the R script and get the output
result = subprocess.run(['Rscript', '--vanilla', 'surfscrape.R'], capture_output=True, text=True)
ht = result.stdout.strip()
while not ht:
    time.sleep(1)
    ht = result.stdout.strip()


import re 
ht = re.search(r'"(.*?)"', ht).group(1)

# Get the current date and time
now = datetime.now()
year = now.year
month = now.month
day = now.day
hour = now.hour
minute = now.minute

# Connect to the SQLite database
conn = sqlite3.connect('db.db')
c = conn.cursor()

# Insert the data into the database
c.execute("INSERT INTO conditions (year, month, day, hour, minute, ht) VALUES (?, ?, ?, ?, ?, ?)", 
          (year, month, day, hour, minute, ht))

# Commit the changes and close the connection
conn.commit()
conn.close()
