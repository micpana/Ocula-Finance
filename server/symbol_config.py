# default risk target divisor
default_risk_target_divisor = 2

# default forecast period
default_forecast_period = 7

# default holding period
default_holding_period = 14 # default = default_forecast_period * 2

# symbols and their config ... targets should be based on the next 7 or 8 candles on the entry timeframe, ours is M15 by default
symbols_and_their_config = {
    # Forex Pairs ***************************************************************************************************************
    'EURUSD': {
        'type': 'Forex Pair',
        'target': 0.15, # manual = 0.25 ... statistical = 0.15
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period,
        'holding_period': default_holding_period
    },
    # 'GBPUSD': {
    #     'type': 'Forex Pair',
    #     'target': 0.12, # manual = 0.30 ... statistical = 0.12
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # }, 
    # 'USDJPY': {
    #     'type': 'Forex Pair',
    #     'target': 0.12, # manual = 0.12 (formerly 0.55) ... statistical = 0.17 (statistical is not performing well)
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # }, 
    # 'USDCHF': {
    #     'type': 'Forex Pair',
    #     'target': 0.16, # manual = 0.30 ... statistical = 0.16
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # }, 
    # 'AUDUSD': {
    #     'type': 'Forex Pair',
    #     'target': 0.17, # manual = 0.40 ... statistical = 0.17
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # }, 
    # 'USDCAD': {
    #     'type': 'Forex Pair',
    #     'target': 0.09, # manual = 0.20 ... statistical = 0.09
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # }, 
    # 'USDZAR': {
    #     'type': 'Forex Pair',
    #     'target': 0.27, # manual = 0.50 ... statistical = 0.27
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # },
    # ***************************************************************************************************************************
    # Crypto Pairs **************************************************************************************************************
    # ***************************************************************************************************************************
    # Synthentic Indices ********************************************************************************************************
    # 'Volatility 75 (1s) Index': {
    #     'type': 'Synthetic Index',
    #     'target': 1.44, # manual = 1.9 ... statistical = 1.44
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # },
    # 'Boom 1000 Index': {
    #     'type': 'Synthetic Index',
    #     'target': 0.39, # manual = (no manual target analysis done) ... statistical = 0.39
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # },
    # 'Crash 1000 Index': {
    #     'type': 'Synthetic Index',
    #     'target': 0.38, # manual = (no manual target analysis done) ... statistical = 0.38
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period,
    #     'holding_period': default_holding_period
    # },
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