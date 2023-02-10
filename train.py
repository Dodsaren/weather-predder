import pandas as pd
from neuralprophet import NeuralProphet, save
from matplotlib import pyplot as plt
from datetime import datetime, timedelta

# Load the data from the CSV file
df = pd.read_csv(
    "data/smhi-opendata_1_124300_20221231_093605.csv", delimiter=';')

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

merged_df = merged_df.rename(columns={'datetime': 'ds', 'temp': 'y'})

merged_df.drop(columns=[col for col in merged_df.columns if col not in [
    'y', 'ds']], inplace=True)

print(merged_df.head(3))

m = NeuralProphet(
    # growth='off',
    # n_lags=24 * 7,
    # n_forecasts=24,
    # changepoints_range=0.95,
    # n_changepoints=30,
    weekly_seasonality=False,
    learning_rate=0.1
)
df_train, df_test = m.split_df(merged_df, freq="H", valid_p=1.0 / 12)
metrics = m.fit(df_train, validation_df=df_test)
test_metrics = m.test(df_test)
forecast = m.predict(merged_df)
fig = m.plot(forecast)
m.plot_components(forecast)
m.plot_parameters()
plt.show()

# save(m, 'mymodel.np')

# forecast = m.predict(merged_df)
# m = m.highlight_nth_step_ahead_of_each_forecast(24)
# fig = m.plot_last_forecast(forecast, include_previous_forecasts=24)

# future = m.make_future_dataframe(merged_df)
# print(future)
# forecast = m.predict(future)
# print(forecast)
# m.plot(forecast)
# plt.show()


# # print(forecast.tail(24 * 5))
# # n.plot(forecast)

# # print(df.tail())
# # print(df.date.unique())
# # print(df.columns)
# # print(df.dtypes)
# # plt.plot(df['datetime'], df['temp'])
