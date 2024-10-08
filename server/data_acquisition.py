from pandas import read_csv
from settings import get_data_collection_days_by_intended_purpose, training_data_source, prediction_data_source
from datetime import datetime
from datetime import timedelta
import pytz
from settings import system_timezone
from symbol_config import get_symbol_config

def acquire_data(symbol, timeframes, call_module): # call module = training / prediction
    # initialize ohlc data dict
    ohlc_data_dict = {}

    # get data collection days according to call module
    data_collection_days = get_data_collection_days_by_intended_purpose(call_module)

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

    # create 'datetime' range objects in system's time zone to avoid the implementation of a local time zone offset
    days_back = data_collection_days
    start_date = datetime.now() - timedelta(days=+days_back)
    end_date = datetime.now()+ timedelta(minutes=+6) # some additional time to make sure all current data is included
    timezone_from = datetime(start_date.year, start_date.month, start_date.day, hour=00, minute=00, second=00, tzinfo=timezone)
    timezone_to = datetime(end_date.year, end_date.month, end_date.day, hour=end_date.hour, minute=end_date.minute, second=end_date.second, tzinfo=timezone)

    # loop through timeframes
    for timeframe in timeframes:
        # get data according to data source ... csv / yahoo / mt5 ... and add it to ohlc data dict
        if data_source == 'csv': 
            from csv_data import csv_fetch_data
            ohlc_data_dict[timeframe] = csv_fetch_data(symbol, timeframe)
        elif data_source == 'yahoo': 
            from yahoo_finance_data import yahoo_fetch_data
            ohlc_data_dict[timeframe] = yahoo_fetch_data(symbol, timeframe, timezone_from, timezone_to)
        elif data_source == 'mt5': 
            from mt5_data import mt5_fetch_data 
            ohlc_data_dict[timeframe] = mt5_fetch_data(symbol, timeframe, timezone_from, timezone_to, symbol_type)

    # return ohlc data dict
    return ohlc_data_dict
