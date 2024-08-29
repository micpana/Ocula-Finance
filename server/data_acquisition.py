from pandas import read_csv

folder = 'datasets/'
columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']

def acquire_data(symbol, timeframes, call_module): # call module = training / prediction
    # initialize ohlc data dict
    ohlc_data_dict = {}
    # loop through timeframes
    for timeframe in timeframes:
        # get data
        ohlc_df_path = folder + symbol + timeframe + ".csv"
        ohlc_df = read_csv(ohlc_df_path, names=columns, encoding='utf-16')
        del ohlc_df['col1']
        del ohlc_df['col2']
        # add timeframe data to data dict
        ohlc_data_dict[timeframe] = ohlc_df

    # return ohlc data dict
    return ohlc_data_dict
