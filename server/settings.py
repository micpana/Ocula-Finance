# list of currency pairs and stocks ... symbols
def get_symbols():
    currency_pairs = [
        'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF'
    ]
    stocks = [

    ]
    symbols = currency_pairs + stocks

    return symbols

# source for training data ... csv / mt5 / yahoo
def training_data_source():
    source = 'csv'

    return source

# source for prediction data ... csv / mt5 / yahoo
def prediction_data_source():
    source = 'yahoo'

    return source

# use closing prices only or not ... closing prices only / all ohlc prices
def use_closing_prices_only():
    use_closing_prices_only = True

    return use_closing_prices_only

# forecast period
def get_forecast_period():
    forecast_period = 7

    return forecast_period

# lookback period
def get_lookback_period():
    lookback_period = 50

    return lookback_period

# get timeframes in use, in descending order
def get_timeframes_in_use():
    timeframes_in_use = ['Daily', 'H4', 'H1', 'M15']

    return timeframes_in_use

# get data collection days by intended purpose
def get_data_collection_days_by_intended_purpose(purpose):
    if purpose == 'training':
        days =  2000 # if available ... if more is available, take all ... else take whats available if reasonable
    elif purpose == 'prediction':
        days = 5

    return days

# get data length by number of days and timeframe
def get_data_length_by_number_of_days_and_timeframe(days, timeframe):
        if timeframe == 'Monthly':
            data_length = int(days / 30) # a month has around 30 days
        elif timeframe == 'Weekly':
            data_length = int(days / 7 ) # a week has 7 days
        elif timeframe == 'Daily':
            data_length = int(days * 1) # self
        elif timeframe == 'H4':
            data_length = int(days * 6) # 6 4hour segments in a day
        elif timeframe == 'H1':
            data_length = int(days * 24) # 24 hours in a day
        elif timeframe == 'M15':
            data_length = int(days * 96) # 96 15m segments in a day
        elif timeframe == 'M5':
            data_length = int(days * 288) # 288 5min segments in a day
        elif timeframe == 'M1':
            data_length = int(days * 1440) # 1140 minutes in a day
        else:
            print('Timeframe not configured:', timeframe)

        # handle instances where the days are so little that Monthly and Weekly will be rounded off to 0 during int conversion
        if data_length == 0:
            data_length = 1
        
        return data_length

# get model bidirectional status ... true / false
def get_model_bidirectional_status():
    use_bidirectional_model = True

    return use_bidirectional_model

# get training price data csvs folder path
def get_training_price_data_csvs_folder_path():
    path = 'datasets/'

    return path

# get training logs folder path
def get_training_logs_folder_path():
    path = 'logs/training logs/'

    return path

# get scalers folder path
def get_scalers_folder_path():
    path = 'scalers/'

    return path

# get models folder path
def get_models_folder_path():
    path = 'models/'

    return path

# get error logs folder path
def get_error_logs_folder_path():
    path = 'logs/error logs/'

    return path