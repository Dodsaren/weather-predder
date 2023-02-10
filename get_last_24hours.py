from datetime import datetime, timedelta
import json
import requests


def get_last_24_hours():
    now = datetime.now()
    result = []
    for i in range(24):
        d = now - timedelta(hours=i+1)
        timestamp = d.timestamp()
        result.append(int(timestamp))
    return result


timestamps = get_last_24_hours()
for ts in timestamps:
    response = requests.get('https://api.openweathermap.org/data/3.0/onecall/timemachine',
                            params={
                                'lat': 62.5283,
                                'lon': 14.1944,
                                'units': 'metric',
                                'dt': ts,
                                'appid': '1b6bfcbc6bb30164be2d34f01c420558'
                            })

    # Parse the JSON response
    data = response.json()

    # Save the data to a file
    with open(f'testdata/result_{ts}.json', 'w') as f:
        json.dump(data, f)
