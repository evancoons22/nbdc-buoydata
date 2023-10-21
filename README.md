# nbdc-buoydata
ML project w/ nbdc buoy data

**See live forecasts [here](https://go-ml-surf-forecast.onrender.com/)!**
**UI built [here](https://github.com/evancoons22/go-mb-surf)**

## data collection
- public buoy data is scraped daily from [national data buoy center](https://www.ndbc.noaa.gov/)
- `update.py` runs daily with nohup 
    -   [data source](https://www.ndbc.noaa.gov)
- buoy readings are stored in a sqlite3 table, and predictions are stored in a remote turso database

## data modeling
- using an LSTM to predict readings from Los Angeles buoy  
- see `model.ipynb`

