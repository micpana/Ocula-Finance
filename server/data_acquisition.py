from pandas import read_csv
from settings import get_data_collection_days_by_intended_purpose, training_data_source, prediction_data_source, backtesting_data_source, get_data_length_by_number_of_days_and_timeframe
from datetime import datetime
from datetime import timedelta
import pytz
from settings import system_timezone
from symbol_config import get_symbol_config
import numpy as np

# data acquisition function ***************************************************************************************************************
def acquire_data(symbol, timeframes, call_module, backtest_start_date, view_window): # call module = training / prediction / backtesting
    # initialize ohlc data dict
    ohlc_data_dict = {}

    # get data source according to call module ... csv / yahoo / mt5
    if call_module == 'training':  data_source = training_data_source(); yahoo_override_synthetic_source = 'csv'
    elif call_module == 'prediction': data_source = prediction_data_source(); yahoo_override_synthetic_source = 'mt5'
    elif call_module == 'backtesting': data_source = backtesting_data_source(); yahoo_override_synthetic_source = 'mt5'

    # get the symbol's symbol type ... Forex Pair / Crypto Pair / Synthetic Index
    symbol_type = get_symbol_config(symbol)['type']

    # if symbol type = Synthetic Index and the data source is yahoo, override it to csv (for training) and mt5 (for prediction)
    if symbol_type == 'Synthetic Index' and data_source == 'yahoo':
        data_source = yahoo_override_synthetic_source

    # set time zone
    timezone = pytz.timezone(system_timezone())

    # loop through timeframes ***************************************************************************************************
    for timeframe in timeframes:
        # get data collection days, and the number of bars needed per timeframe, according to call module and current timeframe
        data_collection_days, number_of_bars_needed = get_data_collection_days_by_intended_purpose(call_module, timeframe, data_source)
        # *************************************************************************************************************

        # create 'datetime' range objects in system's time zone to avoid the implementation of a local time zone offset
        start_date = datetime.now() - timedelta(days=+data_collection_days)
        end_date = datetime.now() + timedelta(days=+7) # some additional days to make sure all current data is included
        timezone_from = datetime(start_date.year, start_date.month, start_date.day, hour=00, minute=00, second=00, tzinfo=timezone)
        timezone_to = datetime(end_date.year, end_date.month, end_date.day, hour=end_date.hour, minute=end_date.minute, second=end_date.second, tzinfo=timezone)
        # *************************************************************************************************************

        """
            MT5 brings in even forming candles, ie ones that haven't closed yet. It's candlestick timestamps marks the candlestick's 
            opening time. Therefore to get data for only closed bars when using mt5, delete the last row.
            Yahoo Finance seems to bring in forming candles as well. Not sure if its timestamp is for the opening or closing. More 
            investigation needed.
        """

        # get data according to data source ... csv / yahoo / mt5 *****************************************************
        if data_source == 'csv': 
            from csv_data import csv_fetch_data
            timeframe_ohlc_df, broker_company_name = csv_fetch_data(symbol, timeframe)
            ohlc_data_dict[timeframe] = timeframe_ohlc_df
        elif data_source == 'yahoo': 
            from yahoo_finance_data import yahoo_fetch_data
            timeframe_ohlc_df, broker_company_name = yahoo_fetch_data(symbol, timeframe, timezone_from, timezone_to)
            ohlc_data_dict[timeframe] = timeframe_ohlc_df.head(-1) # removing the last row since its a bar still forming, as stated above
        elif data_source == 'mt5': 
            from mt5_data import mt5_fetch_data
            timeframe_ohlc_df, broker_company_name = mt5_fetch_data(symbol, timeframe, timezone_from, timezone_to, symbol_type)
            ohlc_data_dict[timeframe] = timeframe_ohlc_df.head(-1) # removing the last row since its a bar still forming, as stated above
        # *************************************************************************************************************

        # modify ohlc data to match number_of_bars_needed in ohlc data dict ... (for predictions only) ****************
        if call_module == 'prediction': ohlc_data_dict[timeframe] = ohlc_data_dict[timeframe].tail(number_of_bars_needed)
        # *************************************************************************************************************

        # if backtest_start_date != None ******************************************************************************
        if backtest_start_date != None and timeframe == 'M15':
            """if calling module is not the backtesting module, it will give a backtest_start_date of None"""
            # get the current timeframe's dates array *******************************************************
            timeframe_dates = ohlc_data_dict[timeframe]['time'].values
            # ***********************************************************************************************
            # get the x main loop's starting index **********************************************************
            x_main_loop_starting_index = view_window + 3  # we start from index = view_window+3 (there's a part in the x engineering loop where we need to consider the 2 last candlesticks as well)
            # ***********************************************************************************************
            # indexes of dates on or before backtest start date *********************************************
            # indexes
            index_of_dates_on_or_before_backtest_start_date = np.where(timeframe_dates <= backtest_start_date)[0]
            # if no indexes were found
            if len(index_of_dates_on_or_before_backtest_start_date) == 0: 
                # notify user
                print('\n\nNo data was found on or before', backtest_start_date, 'for', symbol, timeframe, '.')
                # stop the program
                quit()
            # ***********************************************************************************************
            # get the first matching index ******************************************************************
            # pick the last one, thats the current timeframe's first matching index
            first_matching_index = index_of_dates_on_or_before_backtest_start_date[-1]
            # ***********************************************************************************************
            # get the backtest start index ******************************************************************
            """there has to be enough data before first_matching_index for it to match or exceed x_main_loop_starting_index"""
            backtest_start_index = first_matching_index - x_main_loop_starting_index
            # if backtest_start_index is negative, it means data before backtest_start_date is not enough
            if backtest_start_index < 0: 
                # notify user
                print('\n\nData before', backtest_start_date, 'is insufficient for feature engineering on', symbol, timeframe, '.')
                # stop the program
                quit()
            # ***********************************************************************************************
            # remain only with data relevant to the backtest ************************************************
            ohlc_data_dict[timeframe] = ohlc_data_dict[timeframe].iloc[backtest_start_index:]
            # ***********************************************************************************************
        # *************************************************************************************************************
    # ***************************************************************************************************************************

    # return ohlc data dict, broker_company_name
    return ohlc_data_dict, broker_company_name
# *****************************************************************************************************************************************