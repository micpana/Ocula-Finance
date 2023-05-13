# list of currency pairs and stocks ... symbols
def get_symbols():
    currency_pairs = [
        'EURUSD', 'USDJPY', 'GBPUSD', 'USDCHF'
    ]
    stocks = [

    ]
    symbols = currency_pairs + stocks

    return symbols

# source for training data

# source for prediction data

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