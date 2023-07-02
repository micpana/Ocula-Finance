import yfinance as yf

# get data
def yahoo_fetch_data(symbol, timeframes, data_collection_days):
    # returned columns ... Date, Open, High, Low, Close, Volume, Dividends, Stock Splits

    # set time zone to Harare
    timezone = pytz.timezone("Africa/Harare")

    # create 'datetime' range objects in Harare time zone to avoid the implementation of a local time zone offset
    days_back = data_collection_days
    start_date = datetime.now() - timedelta(days=+days_back)
    end_date = datetime.now()+ timedelta(minutes=+6) # some additional time to make sure all current data is included
    timezone_from = datetime(start_date.year, start_date.month, start_date.day, hour=00, minute=00, second=00, tzinfo=timezone)
    timezone_to = datetime(end_date.year, end_date.month, end_date.day, hour=end_date.hour, minute=end_date.minute, second=end_date.second, tzinfo=timezone)
    
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
        timeframe_ohlc_df = symbol_ticker.history(start=timezone_from, end=timezone_to, interval=interval)

        # if timeframe = H4, modify timeframe_ohlc_df into a 4h timeframe, we collected 1h data since yfinance doesn't have 4h
        if timeframe == 'H4':
            # set the datetime index if its not already set
            timeframe_ohlc_df['time'] = pd.to_datetime(timeframe_ohlc_df['time'])
            timeframe_ohlc_df.set_index('time', inplace=True)
            print(timeframe_ohlc_df.head())

            # turn into H4 df
            h4_df = timeframe_ohlc_df.resample('4H').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})

            # drop any rows with missing data
            h4_df.dropna(inplace=True)

            # reset the indexes if needed
            h4_df.reset_index(inplace=True)

            # set h4 data to timeframe_ohlc_df
            timeframe_ohlc_df = h4_df

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