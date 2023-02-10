import pandas as pd
from datetime import datetime, timedelta

array = [
    'data/smhi-opendata_1_124300_20221231_093605.csv',
    'data/smhi-opendata_1_124300_20230101_171035.csv',
    'data/smhi-opendata_1_124320_20221231_093737.csv',
    'data/smhi-opendata_7_124300_20221231_094927.csv',
    'data/smhi-opendata_25_124300_20221231_095146.csv',
]

df = pd.read_csv(array[0], delimiter=';')
df['datetime'] = pd.to_datetime(
    df['date'].astype(str) + ' ' + df['time'].astype(str))


df = df.sort_values("datetime")

# Hämta första och sista datumet
start_date = df["datetime"].iloc[0]
end_date = df["datetime"].iloc[-1]

# Skapa en lista med alla datum mellan start- och slutdatumet
dates = []
while start_date <= end_date:
    dates.append(start_date)
    start_date += timedelta(hours=1)

# Skapa en ny DataFrame med alla datum
new_df = pd.DataFrame({"datetime": dates})

# Slå samman den nya DataFrame med den gamla
merged_df = pd.merge(new_df, df, on="datetime", how="left")

# Fyll i NaN-värden med värdet från föregående rad
merged_df["temp"].fillna(method="ffill", inplace=True)

print(merged_df)

# Skapa en ny kolumn med datumet för föregående rad
# merged_df["prev_date"] = merged_df["datetime"].shift()

# # Beräkna skillnaden mellan datumen i de två kolumnerna och spara resultatet i en ny kolumn
# merged_df["difference"] = merged_df["datetime"] - merged_df["prev_date"]

# # Skapa en timedelta som motsvarar en timme
# hour = timedelta(hours=1)

# # Filtrera DataFrame med hjälp av boolean mask
# filtered_df = merged_df[merged_df["difference"] > hour]

# # Skriv ut filtrerade DataFrame
# print(filtered_df)
