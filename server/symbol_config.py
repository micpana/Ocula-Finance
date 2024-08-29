# default risk target divisor
default_risk_target_divisor = 2

# default forecast period
default_forecast_period = 8

# symbols and their config ... targets should be based on the next 7 candles on the entry timeframe, ours is M15 by default
symbols_and_their_config = {
    # 'EURUSD': {
    #     'type': 'Forex Pair',
    #     'target': 0.15,
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # },
    'Volatility 75 (1s) Index': {
        'type': 'Synthetic Index',
        'target': 1.9, # 1.8 did extremely well, 1.9 did much better
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    },
    # 'Boom 1000 Index': {
    #     'type': 'Synthetic Index',
    #     'target': 0.44, # 0.44, 0.50, 0.90
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # }
}

def get_symbol_config(symbol):
    # retrieve symbol config
    symbol_config = symbols_and_their_config[symbol]
    # return retrieved symbol config
    return symbol_config

def get_symbol_list():
    # retrieve symbol list
    symbols = list(symbols_and_their_config.keys())
    # return retrieved symbol list
    return symbols