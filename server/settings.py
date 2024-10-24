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
        'user', 'admin', 'free user'
    ]

    return user_roles

# list of user roles exempted from subscribing
def user_roles_exempted_from_subscribing():
    roles = ['admin', 'free user']

    return roles

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

# source for training data ... csv / yahoo (will be overridden if symbol is a synthetic index) / mt5
def training_data_source(): # yahoo will be overridden to csv for synthetic indices
    source = 'csv'

    return source

# source for prediction data ...  csv / yahoo (will be overidden if symbol is a synthetic index) / mt5
def prediction_data_source(): # yahoo will be overridden to mt5 for synthetic indices
    source = 'mt5'

    return source

# mt5 program path according to symbol type ... a program path of None or '' means use the system's default installed mt5 program
def get_mt5_program_path_according_to_symbol_type(symbol_type): # Forex Pair / Crypto Pair / Synthetic Index
    # eg "C:\\Program Files\\MetaTrader 5\\terminal64.exe"
    if symbol_type == 'Forex Pair' or symbol_type == 'Crypto Pair': 
        path = None
    elif symbol_type == 'Synthetic Index':
        path = 'C:\\Program Files\\MetaTrader 5 Terminal\\terminal64.exe'

    return path

# y features type ... buy or sell / minimum maximum
def y_features_type():
    y_type = 'buy or sell'

    return y_type

# whether to send out prediction alerts via telegram or not
def send_out_prediction_alerts_via_telegram():
    send = True

    return send

# whether to trim excessive data from other timeframes before feature engineering or not
def trim_excessive_data_from_other_timeframes_before_feature_engineering():
    trim = True

    return trim

# predictions filter config ... filtering predictions using a probability threshold
def predictions_filter_config():
    # whether to filter or not
    filter_predictions_using_a_probability_threshold = True
    # probability threshold
    prediction_probability_threshold = 0.8 # 1.0 is 100 %

    return filter_predictions_using_a_probability_threshold, prediction_probability_threshold

# config for printing test predictions result arrays
def test_predictions_result_arrays_printing_config():
    # win / lose results
    print_win_lose_results_array = False
    # consecutive wins
    print_consecutive_wins_array = False
    # consecutive losses
    print_consecutive_losses_array = False
    # waiting times array
    print_waiting_times_array = False
    # balances array
    print_balances_array = False

    return print_win_lose_results_array, print_consecutive_wins_array, print_consecutive_losses_array, print_waiting_times_array, print_balances_array

# whether to remove last n (n = forecast value) rows without full forecast or not .. Removing them returns a dataset with true forecast values on the last n rows, which is equal to a good dataset
def remove_last_n_values_without_full_forecast():
    remove = False

    return remove

# whether to save live predictions to the database or not
def save_live_predictions_to_database():
    save = True

    return save

# whether to print live predictions to the console or not
def print_live_predictions_to_console():
    print_ = True

    return print_

# whether to printout timeframe timestamp alignment to the console or not
def printout_timeframe_timestamp_alignment():
    print_ = False

    return print_

# whether to quit after printing out timeframe timestamp alignment to the console or not
def quit_after_printing_out_timeframe_timestamp_alignment():
    quit_ = True

    return quit_

# number of timestamps to printout for alignment verification
def number_of_timestamps_to_printout_for_alignment_verification():
    number = 100

    return number

# if we're using yahoo finance, limit number of days for data collection according to yahoo finance's limits
def yahoo_finance_n_days_limitor(timeframe, days):
    # if timeframe == 'Monthly': if days > : days = # can go back several decades
    # elif timeframe == 'Weekly': if days > : days = # can go back several decades
    # elif timeframe == 'Daily': if days > : days = # can go back several decades
    if timeframe == 'H4' and days >= 730: days = 728 # up to 730 days
    elif timeframe == 'H1' and days >= 730: days = 728 # up to 730 days
    elif timeframe == 'M15' and days >= 60: days = 58 # up to 60 days
    elif timeframe == 'M30' and days >= 60: days = 58 # up to 60 days
    elif timeframe == 'M5' and days >= 60: days = 58 # up to 60 days
    elif timeframe == 'M1' and days >= 7: days = 5 # up to 7 days

    return days

# get data length by number of trading days and timeframe
def get_data_length_by_number_of_days_and_timeframe(days, timeframe):
        if timeframe == 'Monthly': data_length = int(days / 30) # a month has around 30 days
        elif timeframe == 'Weekly': data_length = int(days / 7 ) # a week has 7 days
        elif timeframe == 'Daily': data_length = int(days * 1) # self
        elif timeframe == 'H4': data_length = int(days * 6) # 6 4hour segments in a day
        elif timeframe == 'H1': data_length = int(days * 24) # 24 hours in a day
        elif timeframe == 'M30': data_length = int(days * 48) # 48 40m segments in a day
        elif timeframe == 'M15': data_length = int(days * 96) # 96 15m segments in a day
        elif timeframe == 'M5': data_length = int(days * 288) # 288 5min segments in a day
        elif timeframe == 'M1': data_length = int(days * 1440) # 1440 minutes in a day
        else: print('Timeframe not configured:', timeframe)

        # handle instances where the days are so little that Monthly and Weekly will be rounded off to 0 during int conversion
        if data_length == 0: data_length = 1
        
        return data_length

# get data collection days + trading days needed by intended purpose / call module = training / prediction, the timeframe, and the datasource
def get_data_collection_days_by_intended_purpose(purpose, timeframe, data_source):
    """
        For symbols / instruments that don't trade 7 days a week eg forex pairs and stocks, data retrieved via data_collection_days will not 
        match n(data_collection_days*timeframe's segments in a day) bars due to weekends. Trading holidays have the same effect. Therefore, the 
        difference between data_collection_days count and trading_days_needed count has to take that into consideration.
        data_collection_days -> for building a data collection date range, inclusive of weekends and trading holidays.
        trading days needed -> for determining the number of bars needed after data has been collected
    """

    if purpose == 'training': data_collection_days = 1020; trading_days_needed = None # None if parameter is not in use ... number_of_bars_needed will be used
    elif purpose == 'prediction': data_collection_days = 500; trading_days_needed = None # None if parameter is not in use ... number_of_bars_needed will be used

    # yahoo finance has low data collection n days limits depending on the timeframe... limit max days when using yahoo finance
    if data_source == 'yahoo': data_collection_days = yahoo_finance_n_days_limitor(timeframe, data_collection_days)
    if data_source == 'yahoo' and trading_days_needed != None: trading_days_needed = yahoo_finance_n_days_limitor(timeframe, trading_days_needed)

    # get the number of bars needed by number of trading days needed
    if trading_days_needed == None: number_of_bars_needed = data_collection_days
    else: number_of_bars_needed = get_data_length_by_number_of_days_and_timeframe(trading_days_needed, timeframe)

    return data_collection_days, number_of_bars_needed

# whether to show plots during training or not
def show_plots_during_training():
    show = False

    return show

# whether to save plot images during training or not
def save_plots_during_training():
    save = False

    return save

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

# get label encoder path
def get_label_encoder_path(symbol):
    path = 'label encoders/' + symbol + '-Label-Encoder' + custom_system_extension()

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

