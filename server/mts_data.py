import pandas as pd
import MetaTrader5 as mt5

# get data ********************************************************************************************************************************
def mt5_fetch_data(symbol, timeframe, timezone_from, timezone_to):
    # display data on the MetaTrader 5 package **********************************************************************************
    print("MetaTrader5 package author: ", mt5.__author__)
    print("MetaTrader5 package version: ", mt5.__version__)
    # ***************************************************************************************************************************

    # establish connection to MetaTrader 5 terminal *****************************************************************************
    while True:
        if not mt5.initialize():
            print("initialize() failed, error code =", mt5.last_error())
        else:
            break
    # ***************************************************************************************************************************

    # get data for each stated timeframe ****************************************************************************************
    print('Fetching rates for ', symbol, 'from MT5 ...')
    if timeframe == 'Monthly': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_MN1, timezone_from, timezone_to)
    elif timeframe == 'Weekly': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_W1, timezone_from, timezone_to)
    elif timeframe == 'Daily': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_D1, timezone_from, timezone_to)
    elif timeframe == 'H4': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_H4, timezone_from, timezone_to)
    elif timeframe == 'H1': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_H1, timezone_from, timezone_to)
    elif timeframe == 'M15': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_M15, timezone_from, timezone_to)
    elif timeframe == 'M5': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_M5, timezone_from, timezone_to)
    elif timeframe == 'M1': rates = mt5.copy_rates_range(str(symbol), mt5.TIMEFRAME_M1, timezone_from, timezone_to)
    else: print('Timeframe not configured:', timeframe); quit()
    # ***************************************************************************************************************************

    # shut down connection to the MetaTrader 5 terminal *************************************************************************
    mt5.shutdown()
    # ***************************************************************************************************************************

    # create dataframe out of the obtained data *********************************************************************************
    timeframe_ohlc_df = pd.DataFrame(rates)
    # ***************************************************************************************************************************
    
    # convert time in seconds into the 'datetime' format ************************************************************************
    timeframe_ohlc_df['time'] = pd.to_datetime(timeframe_ohlc_df['time'], unit='s')
    # ***************************************************************************************************************************

    print('MT5 Rates fetched.\n\n')

    # return timeframe ohlc df
    return timeframe_ohlc_df
# *****************************************************************************************************************************************