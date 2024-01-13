from pandas import read_csv
from settings import get_training_price_data_csvs_folder_path, get_error_logs_path, get_data_length_by_number_of_days_and_timeframe

# get data
def csv_fetch_data(symbol, timeframes, data_collection_days):

    # folder and column names
    folder = get_training_price_data_csvs_folder_path()
    columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']

    # initialize variables for timeframe 1, timeframe 2, timeframe 3, timeframe 4, etc... data
    timeframe_1 = None
    timeframe_2 = None
    timeframe_3 = None
    timeframe_4 = None
    timeframe_5 = None
    timeframe_6 = None
    timeframe_7 = None
    timeframe_8 = None

    # get data for each stated timeframe
    for timeframe in timeframes:
        # import timeframe ohlc data
        timeframe_ohlc_file = folder + symbol + timeframe + ".csv"
        timeframe_ohlc_df = read_csv(timeframe_ohlc_file, names=columns, encoding='utf-16')
        del timeframe_ohlc_df['col1']
        del timeframe_ohlc_df['col2']

        # get timeframe number
        timeframe_number = timeframes.index(timeframe) + 1

        # set data to appropriate timeframe variable
        if timeframe_number == 1:
            timeframe_1 = timeframe_ohlc_df
        elif timeframe_number == 2:
            timeframe_2 = timeframe_ohlc_df
        elif timeframe_number == 3:
            timeframe_3 = timeframe_ohlc_df
        elif timeframe_number == 4:
            timeframe_4 = timeframe_ohlc_df
        elif timeframe_number == 5:
            timeframe_5 = timeframe_ohlc_df
        elif timeframe_number == 6:
            timeframe_6 = timeframe_ohlc_df
        elif timeframe_number == 7:
            timeframe_7 = timeframe_ohlc_df
        elif timeframe_number == 8:
            timeframe_8 = timeframe_ohlc_df

    # return data as timeframe 1, timeframe 2, timeframe 3, timeframe 4, timeframe 5, timeframe 6, timeframe 7, timeframe 8
    return timeframe_1, timeframe_2, timeframe_3, timeframe_4, timeframe_5, timeframe_6, timeframe_7, timeframe_8