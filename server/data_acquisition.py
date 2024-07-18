from pandas import read_csv

folder = 'datasets/'
columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']

def acquire_data(symbol, timeframes):
    data_dict = {}
    for timeframe in timeframes:
        # get data
        ohlc_df_path = folder + symbol + timeframe + ".csv"
        ohlc_df = read_csv(ohlc_df_path, names=columns, encoding='utf-16')
        del ohlc_df['col1']
        del ohlc_df['col2']
        # add timeframe data to data dict
        data_dict[timeframe] = ohlc_df

    # return timeframe dataframes from data dict ... Daily, H4, H1, M30, M15
    return data_dict['Daily'], data_dict['H4'], data_dict['H1'], data_dict['M30'], data_dict['M15']
