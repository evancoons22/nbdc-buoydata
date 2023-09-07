import requests
import schedule
import pandas as pd
import numpy as np
import math
import re
import sqlite3

import functions

conn = sqlite3.connect('db.db')
df_main.to_sql('main', conn, if_exists='replace', index=False)
