from pandas import read_csv
from settings import get_training_logs_folder_path, get_error_logs_folder_path

# get data
def csv_fetch_data(symbol, timeframes):

    # folder and column names
    folder = get_training_logs_folder_path()
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'col1', 'col2']

    # get data for each stated timeframe
    for timeframe in timeframes:
        # import timeframe ohlc data
        timeframe_ohlc_file = folder + symbol + timeframe + ".csv"
        timeframe_ohlc_df = read_csv(timeframe_ohlc_file, names=columns, encoding='utf-16')
        del timeframe_ohlc_df['col1']
        del timeframe_ohlc_df['col2']


    # return data as timeframe 1, timeframe 2, timeframe 3, timeframe 4
    return