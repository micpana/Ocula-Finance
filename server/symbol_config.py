# default risk target divisor
default_risk_target_divisor = 2

# default forecast period
default_forecast_period = 14

# default holding period
default_holding_period = 

# symbols and their config ... targets should be based on the next 8 candles on the entry timeframe, ours is M15 by default
symbols_and_their_config = {
    # Forex Pairs ***************************************************************************************************************
    'EURUSD': {
        'type': 'Forex Pair',
        'target': 0.23, # manual = 0.25 ... statistical = 0.23
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period,
        'holding_period': default_holding_period
    },
    'GBPUSD': {
        'type': 'Forex Pair',
        'target': 0.18, # manual = 0.30 ... statistical = 0.18
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    }, 
    'USDJPY': {
        'type': 'Forex Pair',
        'target': 0.28, # manual = 0.55 ... statistical = 0.28
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    }, 
    'USDCHF': {
        'type': 'Forex Pair',
        'target': 0.23, # manual = 0.30 ... statistical = 0.23
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    }, 
    'AUDUSD': {
        'type': 'Forex Pair',
        'target': 0.24, # manual = 0.40 ... statistical = 0.24
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    }, 
    'USDCAD': {
        'type': 'Forex Pair',
        'target': 0.13, # manual = 0.20 ... statistical = 0.13
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    }, 
    'USDZAR': {
        'type': 'Forex Pair',
        'target': 0.39, # manual = 0.50 ... statistical = 0.39
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    },
    # ***************************************************************************************************************************
    # Crypto Pairs **************************************************************************************************************
    # ***************************************************************************************************************************
    # Synthentic Indices ********************************************************************************************************
    'Volatility 75 (1s) Index': {
        'type': 'Synthetic Index',
        'target': 1.9, # manual = 1.9 ... statistical = (symbol was used as statistical sample)
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    },
    # ***************************************************************************************************************************
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