import pandas as pd
from datetime import timedelta


def load(path):
    # Load csv into data frame
    df = pd.read_csv(path, delimiter=';')

    # Create a column of type date by combingin date and time columns
    df['datetime'] = pd.to_datetime(
        df['date'].astype(str) + ' ' + df['time'].astype(str))

    # sort by dates
    df = df.sort_values("datetime")

    # Get first and last date
    start_date = df["datetime"].iloc[0]
    end_date = df["datetime"].iloc[-1]

    # Create an array with all datetimes between start and end (one hour increment)
    dates = []
    while start_date <= end_date:
        dates.append(start_date)
        start_date += timedelta(hours=1)

    # Create a new df with all the datetimes
    new_df = pd.DataFrame({"datetime": dates})

    # merge new dataframe with original
    merged_df = pd.merge(new_df, df, on="datetime", how="left")

    # Fill nan values with value from previous row
    merged_df["temp"].fillna(method="ffill", inplace=True)

    merged_df = merged_df.rename(columns={'datetime': 'ds', 'temp': 'y'})

    merged_df.drop(columns=[col for col in merged_df.columns if col not in [
        'y', 'ds']], inplace=True)

    return merged_df
