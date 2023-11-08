from datetime import datetime

# platform name
def platform_name():
    name = 'Ocula Finance'

    return name

# frontend url
def frontend_client_url():
    url = 'https://oculafinance.com'

    return url

# database selection ... mock / test / live
def database_selection():
    selection = 'mock'

    return selection

# verification token expiration minutes
def verification_token_expiration_minutes():
    expiration_minutes = 15

    return expiration_minutes

# access token expiration days
def access_token_expiration_days():
    expiration_days = 90

    return expiration_days

# token-send on user request retry period in minutes
def token_send_on_user_request_retry_period_in_minutes():
    minutes = 2

    return minutes 

# list of currency pairs and stocks ... symbols
def get_symbols():
    currency_pairs = [
        'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF'
    ]
    stocks = [

    ]
    symbols = currency_pairs + stocks

    return symbols

# list of user roles
def get_user_roles():
    user_roles = [
        'user', 'admin'
    ]

    return user_roles

# list of payment purposes
def get_payment_purposes():
    payment_purposes = ['subscription']

    return payment_purposes

# list of payment methods
def get_payment_methods():
    payment_methods = [
        'Cash', 'Innbucks', 'Ecocash USD', 'Paypal', 'Bitcoin', 'Ethereum'
    ]

    return payment_methods

# increment number for client load more feature
def get_client_load_more_increment():
    client_load_more_increment = 50

    return client_load_more_increment

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

# get custom system extension for saving objects as files
def custom_system_extension():
    extension = '.ocula_finance'

    return extension

# get training price data csvs folder path
def get_training_price_data_csvs_folder_path():
    path = 'datasets/'

    return path

# universal filename append string for model object files
def universal_filename_append_string(timeframes, features_type, model_type, with_extension):
    if with_extension == True:
        string = '-' + model_type + ' Model-' + features_type + '-' + str(timeframes) + custom_system_extension()
    else:
        string = '-' + model_type + ' Model-' + features_type + '-' + str(timeframes)

    return string

# get training logs path
def get_training_logs_path(symbol, timeframes, features_type, model_type):
    path = 'logs/training logs/' + symbol + '-Training Log-' + str(datetime.now()) + universal_filename_append_string(timeframes, features_type, model_type, True)

    return path

# get scalers path
def get_scalers_path(symbol, timeframes, features_type, model_type, scaler_set):
    if scaler_set == 'x':
        path = 'scalers/' + symbol + '-X Scaler' + universal_filename_append_string(timeframes, features_type, model_type, True)
    elif scalers == 'y':
        path = 'scalers/' + symbol + '-Y Scaler' + universal_filename_append_string(timeframes, features_type, model_type, True)

    return path

# get models path
def get_models_path(symbol, timeframes, features_type, model_type):
    path = 'models/' + symbol + universal_filename_append_string(timeframes, features_type, model_type, True)

    return path

# get models checkpoints path
def get_models_checkpoints_path(symbol, timeframes, features_type, model_type):
    path = 'models checkpoints/' + 'weights' + universal_filename_append_string(timeframes, features_type, model_type, False) + '.best' + '.hdf5' 

    return path

# get error logs path
def get_error_logs_path(name):
    path = 'logs/error logs/' + 'Log-' + name + '-' + str(datetime.now()) + '.txt'

    return path

# get cookies path
def get_cookies_path(name):
    path = 'cookies/' + name + custom_system_extension()

    return path