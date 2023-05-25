import yfinance as yf

# get data
def yahoo_fetch_data(symbol, timeframes, data_collection_days):
    # returned columns ... Date, Open, High, Low, Close, Volume, Dividends, Stock Splits

    # Set the range and interval
    start_date = '2022-01-01'
    end_date = '2022-12-01'
    
    # initialize variables for timeframe 1, timeframe 2, timeframe 3, timeframe 4 data
    timeframe_1 = None
    timeframe_2 = None
    timeframe_3 = None
    timeframe_4 = None

    # get data for each stated timeframe
    for timeframe in timeframes:
        # set interval ... valid = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        if timeframe == 'Monthly':
            interval = '1mo'
        elif timeframe == 'Weekly':
            interval = '1wk'
        elif timeframe == 'Daily':
            interval = '1d'
        elif timeframe == 'H4':
            interval = '1h' # yfinance has no 4hour timeframe
        elif timeframe == 'H1':
            interval = '1h'
        elif timeframe == 'M15':
            interval = '15m'
        elif timeframe == 'M5':
            interval = '5m'
        elif timeframe == 'M1':
            interval = '1m'
        else:
            print('Timeframe not configured:', timeframe)
            quit()

        # Get the OHLC data
        symbol_ticker = yf.Ticker(symbol+'=X')
        timeframe_ohlc_df = symbol_ticker.history(start=start_date, end=end_date, interval=interval)

        # if timeframe = H4, modify timeframe_ohlc_df into a 4h timeframe, we collected 1h data since yfinance doesn't have 4h

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