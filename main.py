import pandas as pd
from neuralprophet import NeuralProphet, load
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import json
import requests
import sys
import os
import pytz

# Create an empty dataframe
df = pd.DataFrame(columns=['y', 'ds'])

# Get the list of files in the directory
files = os.listdir('testdata')

# Loop over the files
for file in files:
    # Read the file
    with open(f'testdata/{file}', 'r') as f:
        data = f.read()

    # Parse the JSON data
    data = json.loads(data)

    # Get the temp and dt values from the data
    y = data['data'][0]['temp']
    ds = data['data'][0]['dt']

    # Add the data to the dataframe
    df = pd.concat(
        [df, pd.DataFrame({'y': y, 'ds': ds}, index=[0])], ignore_index=True)

# Convert the ds column to UTC
df['ds'] = df['ds'].apply(lambda x: datetime.utcfromtimestamp(x))
df.sort_values('ds', inplace=True)

print(df)

m = load('mymodel.np')

future = m.make_future_dataframe(df)
forecast = m.predict(future)
fdf = m.get_latest_forecast(forecast)


# Get the timezone object for Stockholm
stockholm_tz = pytz.timezone('Europe/Stockholm')
fdf['ds'] = fdf['ds'].dt.tz_localize('UTC')
# Convert the UTC date to the Stockholm timezone
fdf['ds'] = fdf['ds'].apply(
    lambda x: stockholm_tz.normalize(x.astimezone(stockholm_tz)))
print(fdf)


# m = m.highlight_nth_step_ahead_of_each_forecast(24)
# fig = m.plot_last_forecast(forecast, include_previous_forecasts=10)
# plt.show()
