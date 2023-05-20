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

# use closing prices only or not
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

# get data length by intended purpose
def get_data_length_by_intended_purpose(purpose):
    if purpose == 'training':
        data_length = 30000 # if available ... if more is available, take all ... else take whats available if reasonable
    elif purpose == 'prediction':
        data_length = 100

# get training price data csvs folder path
def get_training_price_data_csvs_folder_path():
    path = 'training csvs/'

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