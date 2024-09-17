import pandas as pd
import MetaTrader5 as mt5
from datetime import datetime
from datetime import timedelta
import pytz
from settings import system_timezone

# get data
def mt5_fetch_data(symbol, timeframes, data_collection_days):
    # display data on the MetaTrader 5 package
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)

    # establish connection to MetaTrader 5 terminal
    while True:
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
        else:
            break

    # set time zone
    timezone = pytz.timezone(system_timezone())

    # create 'datetime' range objects in Harare time zone to avoid the implementation of a local time zone offset
    days_back = data_collection_days
    start_date = datetime.now() - timedelta(days=+days_back)
    end_date = datetime.now()+ timedelta(minutes=+6) # some additional time to make sure all current data is included
    timezone_from = datetime(start_date.year, start_date.month, start_date.day, hour=00, minute=00, second=00, tzinfo=timezone)
    timezone_to = datetime(end_date.year, end_date.month, end_date.day, hour=end_date.hour, minute=end_date.minute, second=end_date.second, tzinfo=timezone)

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
    print('Fetching rates for ', symbol, 'from MT5 ...')
    for timeframe in timeframes:
        if timeframe == 'Monthly':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_MN1, timezone_from, timezone_to)
        elif timeframe == 'Weekly':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_W1, timezone_from, timezone_to)
        elif timeframe == 'Daily':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_D1, timezone_from, timezone_to)
        elif timeframe == 'H4':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_H4, timezone_from, timezone_to)
        elif timeframe == 'H1':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_H1, timezone_from, timezone_to)
        elif timeframe == 'M15':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_M15, timezone_from, timezone_to)
        elif timeframe == 'M5':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_M5, timezone_from, timezone_to)
        elif timeframe == 'M1':
            rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_M1, timezone_from, timezone_to)
        else:
            print('Timeframe not configured:', timeframe)
            quit()

        # shut down connection to the MetaTrader 5 terminal
        mt5.shutdown()

        # create dataframe out of the obtained data
        timeframe_ohlc_df = pd.DataFrame(rates)
        
        # convert time in seconds into the 'datetime' format
        timeframe_ohlc_df['time'] = pd.to_datetime(timeframe_ohlc_df['time'], unit='s')

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

    print('MT5 Rates fetched.\n\n')

    # return data as timeframe 1, timeframe 2, timeframe 3, timeframe 4, timeframe 5, timeframe 6, timeframe 7, timeframe 8
    return timeframe_1, timeframe_2, timeframe_3, timeframe_4, timeframe_5, timeframe_6, timeframe_7, timeframe_8