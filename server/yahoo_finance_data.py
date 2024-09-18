import pandas as pd
import yfinance as yf

# get data ********************************************************************************************************************************
def yahoo_fetch_data(symbol, timeframe, timezone_from, timezone_to):
    # returned columns => Date/Datetime, Open, High, Low, Close, Volume, Dividends, Stock Splits

    # set interval ... valid = 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo ****************************************
    if timeframe == 'Monthly': interval = '1mo'; date_column_name = ''
    elif timeframe == 'Weekly': interval = '1wk'; date_column_name = ''
    elif timeframe == 'Daily': interval = '1d'; date_column_name = 'Date'
    elif timeframe == 'H4': interval = '1h'; date_column_name = 'Datetime' # yfinance has no 4hour timeframe, we'll collect 1hour data and then aggregate
    elif timeframe == 'H1': interval = '1h'; date_column_name = 'Datetime'
    elif timeframe == 'M15': interval = '15m'; date_column_name = 'Datetime'
    elif timeframe == 'M5': interval = '5m'; date_column_name = 'Datetime'
    elif timeframe == 'M1': interval = '1m'; date_column_name = 'Datetime'
    else: print('Timeframe not configured:', timeframe); quit()
    # ***************************************************************************************************************************

    # Get the OHLC data *********************************************************************************************************
    symbol_ticker = yf.Ticker(symbol+'=X')
    timeframe_ohlc_df = symbol_ticker.history(start=timezone_from, end=timezone_to, interval=interval)
    # ***************************************************************************************************************************
    
    # reset index into a column and rename columns to match those in mt5_data.py ************************************************
    timeframe_ohlc_df.reset_index(inplace=True)
    timeframe_ohlc_df = timeframe_ohlc_df.rename(
        columns={date_column_name: 'time', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close'}
    )
    # ***************************************************************************************************************************

    # if timeframe = H4, modify timeframe_ohlc_df into a 4h timeframe, we collected 1h data since yfinance doesn't have 4h ******
    if timeframe == 'H4':
        # set the datetime index if its not already set
        timeframe_ohlc_df['time'] = pd.to_datetime(timeframe_ohlc_df['time'])
        timeframe_ohlc_df.set_index('time', inplace=True)

        # turn into H4 df
        h4_df = timeframe_ohlc_df.resample('4H').agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})

        # drop any rows with missing data
        h4_df.dropna(inplace=True)

        # reset the indexes if needed
        h4_df.reset_index(inplace=True)

        # set h4 data to timeframe_ohlc_df
        timeframe_ohlc_df = h4_df
    # ***************************************************************************************************************************

    # return timeframe ohlc df
    return timeframe_ohlc_df
# *****************************************************************************************************************************************