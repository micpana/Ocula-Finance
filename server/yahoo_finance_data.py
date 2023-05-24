# get data
def yahoo_fetch_data(symbol, timeframes, preferred_minimum_data_count):
    
    # initialize variables for timeframe 1, timeframe 2, timeframe 3, timeframe 4 data
    timeframe_1 = None
    timeframe_2 = None
    timeframe_3 = None
    timeframe_4 = None

    # get data for each stated timeframe
    for timeframe in timeframes:

        # set data to appropriate timeframe variable
        timeframe_number = timeframes.index(timeframe) + 1
        if timeframe_number == 1:
            timeframe_1 = timeframe_ohlc_df
        elif timeframe_number == 2:
            timeframe_2 = timeframe_ohlc_df
        elif timeframe_number == 3:
            timeframe_3 = timeframe_ohlc_df
        elif timeframe_number == 4:
            timeframe_4 = timeframe_ohlc_df

    # return data as timeframe 1, timeframe 2, timeframe 3, timeframe 4
    return timeframe_1, timeframe_2, timeframe_3, timeframe_4