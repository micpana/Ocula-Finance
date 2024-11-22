import pandas as pd
import MetaTrader5 as mt5
from settings import get_mt5_program_path_according_to_symbol_type

# get data ********************************************************************************************************************************
def mt5_fetch_data(symbol, timeframe, timezone_from, timezone_to, symbol_type):
    print('Fetching', symbol, timeframe, 'data from MT5 ...')
    
    # display data on the MetaTrader 5 package **********************************************************************************
    # print("MetaTrader5 package author: ", mt5.__author__)
    # print("MetaTrader5 package version: ", mt5.__version__)
    # ***************************************************************************************************************************

    # mt5 program path according to symbol type *********************************************************************************
    mt5_program_path = get_mt5_program_path_according_to_symbol_type(symbol_type)
    # ***************************************************************************************************************************

    # establish connection to MetaTrader 5 terminal *****************************************************************************
    while True:
        # if program path is None or '', use the system's default installed mt5 program
        if mt5_program_path == None or mt5_program_path == '':
            if not mt5.initialize(): print("initialize() failed, error code =", mt5.last_error())
            else: break
        # if a program path was supplied
        else:
            if not mt5.initialize(mt5_program_path): print("initialize() failed, error code =", mt5.last_error())
            else: break
    # ***************************************************************************************************************************

    # get broker's company name *************************************************************************************************
    # retrieve terminal information ***********************************************************************************
    terminal_info = mt5.terminal_info()
    # *****************************************************************************************************************
    # check if the information was retrieved successfully *************************************************************
    if terminal_info is not None:
        broker_company_name = terminal_info.company
        print(f"Broker's Company Name: {broker_company_name}")
    else:
        broker_company_name = 'Failed to retrieve'
        print(f"Failed to retrieve terminal info, error code: {mt5.last_error()}")
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # get data for each stated timeframe ****************************************************************************************
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
    # print('df head:\n', timeframe_ohlc_df.head(10))
    # ***************************************************************************************************************************

    # convert time in seconds into the 'datetime' format ************************************************************************
    # conversion
    timeframe_ohlc_df['time'] = pd.to_datetime(timeframe_ohlc_df['time'], unit='s')
    # make sure the datetime is in our required format
    timeframe_ohlc_df['time'] = timeframe_ohlc_df['time'].dt.strftime('%Y.%m.%d %H:%M')
    # ***************************************************************************************************************************

    print('MT5 data fetched.\n\n')

    # return timeframe ohlc df, broker_company_name
    return timeframe_ohlc_df, broker_company_name
# *****************************************************************************************************************************************