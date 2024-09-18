from datetime import datetime
from pytz import timezone

# platform name
def platform_name():
    name = 'Ocula Finance'

    return name

# frontend url
def frontend_client_url():
    url = 'https://oculafinance.com' # main url
    # url = 'https://oculafinance.netlify.app' # test url

    return url

# sending emails via ... zoho mail / gmail test smtp
def sending_emails_via():
    send_via = 'zoho mail'

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

# source for training data ... csv / yahoo / mt5
def training_data_source():
    source = 'csv'

    return source

# source for prediction data ... csv / yahoo / mt5
def prediction_data_source():
    source = 'mt5'

    return source

# whether to remove last n (n = forecast value) rows without full forecast or not .. Removing them returns a dataset with true forecast values on the last n rows, which is equal to a good dataset
def remove_last_n_values_without_full_forecast():
    remove = False

    return remove

# whether to save live predictions to the database or not
def save_live_predictions_to_database():
    save = False

    return save

# whether to print live predictions to the console or not
def print_live_predictions_to_console():
    print_ = True

    return print_

# get data collection days by intended purpose / call module = training / prediction
def get_data_collection_days_by_intended_purpose(purpose):
    if purpose == 'training':
        days =  2000 # if available ... if more is available, take all ... else take whats available if reasonable
    elif purpose == 'prediction':
        days = 200

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
            data_length = int(days * 1440) # 1440 minutes in a day
        else:
            print('Timeframe not configured:', timeframe)

        # handle instances where the days are so little that Monthly and Weekly will be rounded off to 0 during int conversion
        if data_length == 0:
            data_length = 1
        
        return data_length

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

# get training logs path
def get_training_log_path(symbol):
    path = 'logs/training logs/' + symbol + '-Training-Log.json'

    return path

# get scalers path
def get_scaler_path(symbol):
    path = 'scalers/' + symbol + '-Scaler' + custom_system_extension()

    return path

# get models path
def get_model_path(symbol):
    path = 'models/' + symbol + '-Model' + custom_system_extension()

    return path

# get error logs path
def get_error_logs_path(name):
    path = 'logs/error logs/' + 'Log-' + name + '-' + str(datetime.now(timezone(system_timezone()))) + '.txt'

    return path

# get model performance visual insights path
def get_model_performance_visual_insights_path(symbol, name):
    path = 'model performance visual insights/' + symbol + ' - ' + name + '.png'

    return path

# get cookies path
def get_cookies_path(name):
    path = 'cookies/' + name + custom_system_extension()

    return path

# extension for encrypted code files
def encrypted_code_files_extension():
    extension = custom_system_extension() + '_code'

    return extension

# encypted x y feature engineering object path
def get_x_y_feature_engineering_object_path():
    path = 'x_y_feature_engineering' + encrypted_code_files_extension()

    return path

# encypted x feature engineering object path
def get_x_feature_engineering_object_path():
    path = 'x_feature_engineering' + encrypted_code_files_extension()

    return path

# encypted y feature engineering object path
def get_y_feature_engineering_object_path():
    path = 'y_feature_engineering' + encrypted_code_files_extension()

    return path

# encypted x y training object path
def get_x_y_training_object_path():
    path = 'x_y_train' + encrypted_code_files_extension()

    return path

# encrypted x y prediction object path
def get_x_y_prediction_object_path():
    path = 'x_y_predict' + encrypted_code_files_extension()

    return path

# encrypted manage expired open trades object path
def get_manage_expired_open_trades_object_path():
    path = 'manage_expired_open_trades' + encrypted_code_files_extension()

    return path

# encrypted unknown object path
def get_unknown_object_path():
    path = 'encrypted_code' + encrypted_code_files_extension()

    return path

