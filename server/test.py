from pandas import read_csv
import pandas as pd

columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']
ohlc_file = "datasets/H1.csv"
ohlc_df = read_csv(ohlc_file, names=columns, encoding='utf-16')
del ohlc_df['col1']
del ohlc_df['col2']

print(ohlc_df.head())

# set the datetime index if its not already set
ohlc_df['time'] = pd.to_datetime(ohlc_df['time'])
ohlc_df.set_index('time', inplace=True)
print(ohlc_df.head())

# turn into H4 df
h4_df = ohlc_df.resample('4H').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})

# drop any rows with missing data
h4_df.dropna(inplace=True)

# reset the indexes if needed
h4_df.reset_index(inplace=True)

print(h4_df['time'])