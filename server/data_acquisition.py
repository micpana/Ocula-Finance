from pandas import read_csv
from csv_data import csv_fetch_data
from yahoo_finance_data import yahoo_fetch_data
from mt5_data import mt5_fetch_data
from settings import get_data_collection_days_by_intended_purpose, training_data_source, prediction_data_source
from datetime import datetime
from datetime import timedelta
import pytz
from settings import system_timezone

def acquire_data(symbol, timeframes, call_module): # call module = training / prediction
    # initialize ohlc data dict
    ohlc_data_dict = {}

    # get data collection days according to call module
    data_collection_days = get_data_collection_days_by_intended_purpose(call_module)

    # get data source according to call module
    if call_module == 'training':  data_source = training_data_source()
    elif call_module == 'prediction': data_source = prediction_data_source()

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
        if data_source == 'csv': ohlc_data_dict[timeframe] = csv_fetch_data(symbol, timeframe)
        elif data_source == 'yahoo': ohlc_data_dict[timeframe] = yahoo_fetch_data(symbol, timeframe, timezone_from, timezone_to)
        elif data_source == 'mt5': ohlc_data_dict[timeframe] = mt5_fetch_data(symbol, timeframe, timezone_from, timezone_to)

    # return ohlc data dict
    return ohlc_data_dict
