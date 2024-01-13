from datetime import datetime
from pytz import timezone

# platform name
def platform_name():
    name = 'Ocula Finance'

    return name

# frontend url
def frontend_client_url():
    # url = 'https://oculafinance.com' # main url
    url = 'https://oculafinance.netlify.app' # test url

    return url

# sending emails via ... mailjet / gmail test smtp
def sending_emails_via():
    send_via = 'gmail test smtp'

    return send_via

# database selection ... mock / test / live
def database_selection():
    selection = 'live'

    return selection

# system timezone ... pytz compatible
def system_timezone():
    sys_timezone = 'Africa/Harare'

    return sys_timezone

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

# number of free trial days
def get_number_of_free_trial_days():
    days = 7

    return days

# list of currency pairs and stocks ... symbols
def get_symbols():
    currency_pairs = [
        'EURUSD'
        # , 'USDJPY', 'GBPUSD', 'USDCHF', 'USDZAR'
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

# run predictions module as flask thread or not
def run_predictions_as_flask_thread():
    run = False

    return run

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
    lookback_period = 300

    return lookback_period

# get timeframes in use, in descending order ... max 8 timeframes, min 1 timeframe
def get_timeframes_in_use():
    timeframes_in_use = [
        # 'Monthly',
        # 'Weekly',
        'Daily', 
        'H4', 
        'H1', 
        'M15',
        'M5',
        'M1'
    ]

    return timeframes_in_use

# get entry timeframe ... should be part of the timeframes_in_use list
def get_entry_timeframe():
    entry_timeframe = 'M15'

    return entry_timeframe

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

# index of model to use
def index_of_model_to_use():
    index = 1

    return index

# whether to use percentage changes or price on x data
def x_use_percentages():
    use = False

    return use

# whether to use percentage changes or price on y data 
def y_use_percentages():
    use = True

    return use

# get scaler x status
def scale_x():
    scale_x = True

    return scale_x

# get scaler y status
def scale_y():
    scale_y = False

    return scale_y

# whether to show plots during training or not
def show_plots_during_training():
    show = True

    return show

# get custom system extension for saving objects as files
def custom_system_extension():
    extension = '.ocula_finance'

    return extension

# get training price data csvs folder path
def get_training_price_data_csvs_folder_path():
    path = 'datasets/'

    return path

# universal filename append string for model object files
def universal_filename_append_string(timeframes, features_type, with_extension):
    if with_extension == True:
        string = '-MI:' + str(index_of_model_to_use()) + '-Model-' + features_type + '-TF' + str(timeframes) + '-ET:' + get_entry_timeframe() + '-L' + str(get_lookback_period()) + ':F' + str(get_forecast_period()) + '-XS' + str(scale_x()) + ':YS' + str(scale_y()) + '-XUP' + str(x_use_percentages()) + ':YUP' + str(y_use_percentages()) + custom_system_extension()
    else:
        string = '-MI:' + str(index_of_model_to_use()) + '-Model-' + features_type + '-TF' + str(timeframes) + '-ET:' + get_entry_timeframe() + '-L' + str(get_lookback_period()) + ':F' + str(get_forecast_period()) + '-XS' + str(scale_x()) + ':YS' + str(scale_y()) + '-XUP' + str(x_use_percentages()) + ':YUP' + str(y_use_percentages())

    return string

# get training logs path
def get_training_logs_path(symbol, timeframes, features_type):
    path = 'logs/training logs/' + symbol + '-Training Log-' + str(datetime.now(timezone(system_timezone()))) + universal_filename_append_string(timeframes, features_type, True)

    return path

# get scalers path
def get_scalers_path(symbol, timeframes, features_type, scaler_set):
    if scaler_set == 'x':
        path = 'scalers/' + symbol + '-X Scaler' + universal_filename_append_string(timeframes, features_type, True)
    elif scaler_set == 'y':
        path = 'scalers/' + symbol + '-Y Scaler' + universal_filename_append_string(timeframes, features_type, True)

    return path

# get models path
def get_models_path(symbol, timeframes, features_type):
    if index_of_model_to_use() == 2 or index_of_model_to_use() == 3: # models that do one output at a time
        path_y_1 = 'models/' + symbol + '-Y1' + universal_filename_append_string(timeframes, features_type, True)
        path_y_2 = 'models/' + symbol + '-Y2' + universal_filename_append_string(timeframes, features_type, True)

        return path_y_1, path_y_2

    else: # models that can do multiple outputs at a time
        path = 'models/' + symbol + universal_filename_append_string(timeframes, features_type, True)

        return path

# get models checkpoints path
def get_models_checkpoints_path(symbol, timeframes, features_type):
    path = 'models checkpoints/' + 'weights' + universal_filename_append_string(timeframes, features_type, False) + '.best' + '.hdf5' 

    return path

# get error logs path
def get_error_logs_path(name):
    path = 'logs/error logs/' + 'Log-' + name + '-' + str(datetime.now(timezone(system_timezone()))) + '.txt'

    return path

# get cookies path
def get_cookies_path(name):
    path = 'cookies/' + name + custom_system_extension()

    return path

# extension for encrypted code files
def encrypted_code_files_extension():
    extension = custom_system_extension() + '_code'

    return extension

# encypted feature engineering object path
def get_feature_engineering_object_path():
    path = 'feature_engineering' + encrypted_code_files_extension()

    return path

# encypted training object path
def get_training_object_path():
    path = 'train' + encrypted_code_files_extension()

    return path

# encrypted prediction object path
def get_prediction_object_path():
    path = 'predict' + encrypted_code_files_extension()

    return path

# encrypted data object path
def get_data_object_path():
    path = 'data' + encrypted_code_files_extension()

    return path

# encrypted unknown object path
def get_unknown_object_path():
    path = 'encrypted_code' + encrypted_code_files_extension()

    return path

