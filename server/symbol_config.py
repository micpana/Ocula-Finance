# default risk target divisor
default_risk_target_divisor = 2

# default forecast period
default_forecast_period = 14

# symbols and their config ... targets should be based on the next 8 candles on the entry timeframe, ours is M15 by default
symbols_and_their_config = {
    # Forex Pairs ***************************************************************************************************************
    'EURUSD': {
        'type': 'Forex Pair',
        'target': 0.25,
        'risk_target_divisor': default_risk_target_divisor,
        'forecast_period': default_forecast_period
    },
    # 'GBPUSD': {
    #     'type': 'Forex Pair',
    #     'target': 0.30,
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # }, 
    # 'USDJPY': {
    #     'type': 'Forex Pair',
    #     'target': 0.50,
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # }, 
    # 'USDCHF': {
    #     'type': 'Forex Pair',
    #     'target': 0.30,
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # }, 
    # 'AUDUSD': {
    #     'type': 'Forex Pair',
    #     'target': 0.40,
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # }, 
    # 'USDCAD': {
    #     'type': 'Forex Pair',
    #     'target': 0.20,
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # }, 
    # 'USDZAR': {
    #     'type': 'Forex Pair',
    #     'target': 0.50,
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
    # },
    # ***************************************************************************************************************************
    # Crypto Pairs (to be added) ************************************************************************************************
    # ***************************************************************************************************************************
    # Synthentic Indices (disabled for now) *************************************************************************************
    # 'Volatility 75 (1s) Index': {
    #     'type': 'Synthetic Index',
    #     'target': 1.9, # 1.8 did extremely well, 1.9 did much better
    #     'risk_target_divisor': default_risk_target_divisor,
    #     'forecast_period': default_forecast_period
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