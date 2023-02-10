import pandas as pd
from neuralprophet import NeuralProphet, save, load
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import data

df = data.load("data/smhi-opendata_1_124300_20221231_093605.csv")

m = NeuralProphet(learning_rate=0.1)
df_train, df_test = m.split_df(df=df, valid_p=0.2)

metrics_train = m.fit(df=df_train, progress='plot')
metrics_test = m.test(df=df_test)

print(metrics_test)
