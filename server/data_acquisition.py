from pandas import read_csv
from settings import get_data_collection_days_by_intended_purpose, training_data_source, prediction_data_source, get_data_length_by_number_of_days_and_timeframe
from datetime import datetime
from datetime import timedelta
import pytz
from settings import system_timezone
from symbol_config import get_symbol_config

def acquire_data(symbol, timeframes, call_module): # call module = training / prediction
    # initialize ohlc data dict
    ohlc_data_dict = {}

    # get data source according to call module ... csv / yahoo / mt5
    if call_module == 'training':  data_source = training_data_source(); yahoo_override_synthetic_source = 'csv'
    elif call_module == 'prediction': data_source = prediction_data_source(); yahoo_override_synthetic_source = 'mt5'

    # get the symbol's symbol type ... Forex Pair / Crypto Pair / Synthetic Index
    symbol_type = get_symbol_config(symbol)['type']

    # if symbol type = Synthetic Index and the data source is yahoo, override it to csv (for training) and mt5 (for prediction)
    if symbol_type == 'Synthetic Index' and data_source == 'yahoo':
        data_source = yahoo_override_synthetic_source

    # set time zone
    timezone = pytz.timezone(system_timezone())

    # loop through timeframes
    for timeframe in timeframes:
        # get data collection days, and the number of bars needed per timeframe, according to call module and current timeframe
        data_collection_days, number_of_bars_needed = get_data_collection_days_by_intended_purpose(call_module, timeframe, data_source)

        # create 'datetime' range objects in system's time zone to avoid the implementation of a local time zone offset
        start_date = datetime.now() - timedelta(days=+data_collection_days)
        end_date = datetime.now() + timedelta(minutes=+6) # some additional time to make sure all current data is included
        timezone_from = datetime(start_date.year, start_date.month, start_date.day, hour=00, minute=00, second=00, tzinfo=timezone)
        timezone_to = datetime(end_date.year, end_date.month, end_date.day, hour=end_date.hour, minute=end_date.minute, second=end_date.second, tzinfo=timezone)

        """
            MT5 brings in even forming candles, ie ones that haven't closed yet. It's candlestick timestamps marks the candlestick's 
            opening time. Therefore to get data for only closed bars when using mt5, delete the last row.
            Yahoo Finance seems to bring in forming candles as well. Not sure if its timestamp is for the opening or closing. More 
            investigation needed.
        """

        # get data according to data source ... csv / yahoo / mt5 ... and add it to ohlc data dict according to number_of_bars_needed (for predictions only)
        if data_source == 'csv': 
            from csv_data import csv_fetch_data
            ohlc_data_dict[timeframe] = csv_fetch_data(symbol, timeframe)
            if call_module == 'prediction': ohlc_data_dict[timeframe] = ohlc_data_dict[timeframe].tail(number_of_bars_needed)
        elif data_source == 'yahoo': 
            from yahoo_finance_data import yahoo_fetch_data
            ohlc_data_dict[timeframe] = yahoo_fetch_data(symbol, timeframe, timezone_from, timezone_to).head(-1) # removing the last row since its a bar still forming, as stated above
            if call_module == 'prediction': ohlc_data_dict[timeframe] = ohlc_data_dict[timeframe].tail(number_of_bars_needed)
        elif data_source == 'mt5': 
            from mt5_data import mt5_fetch_data
            ohlc_data_dict[timeframe] = mt5_fetch_data(symbol, timeframe, timezone_from, timezone_to, symbol_type).head(-1) # removing the last row since its a bar still forming, as stated above
            if call_module == 'prediction': ohlc_data_dict[timeframe] = ohlc_data_dict[timeframe].tail(number_of_bars_needed)

    # return ohlc data dict
    return ohlc_data_dict
