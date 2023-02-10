import data
from matplotlib import pyplot as plt

df = data.load('data/smhi-opendata_1_124300_20230101_171035.csv')
print(df.tail())
df.plot(x='ds', y='y')
plt.show()
