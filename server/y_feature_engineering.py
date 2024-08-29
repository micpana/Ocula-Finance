from collections import deque
import pandas as pd
import numpy as np
from tqdm import tqdm
from symbol_config import get_symbol_config

def engineer_y(x_features_dataframe, y_type, entry_timeframe, symbol):

    # get symbol data ***********************************************************************************************************
    # get symbol config
    symbol_config = get_symbol_config(symbol)

    # reward ... minimum buy or sell target percentage
    reward = symbol_config['target']

    # risk target divisor
    risk_target_divisor = symbol_config['risk_target_divisor']

    # risk 
    risk = reward / risk_target_divisor

    # risk:reward
    risk_to_reward_ratio = '1:'+str(risk_target_divisor)
    
    # forecast period
    forecast_period = symbol_config['forecast_period']
    # ***************************************************************************************************************************

    # get entry timeframes high, low, and closing prices
    entry_timeframe_highs = x_features_dataframe[entry_timeframe+'_High'].values
    entry_timeframe_lows = x_features_dataframe[entry_timeframe+'_Low'].values
    entry_timeframe_closes = x_features_dataframe[entry_timeframe+'_Close'].values
    
    y_dict = {
        'Max % Down': deque([]),
        'Max % Up': deque([])
    }

    # get y column list ... target  variables
    y_column_list = list(y_dict.keys())

    # add extra y column for alternative use other than being the target variable
    y_dict["Trade's Session Closing %"] = deque([])

    # generate y features
    for i in tqdm(range(len(entry_timeframe_closes)), desc="Y Feature Engineering", unit="row"):
        # get entry timeframe's current close
        entry_timeframe_close = entry_timeframe_closes[i]

        # possible lowest price
        lowest_price_in_the_next_forecast_period = np.min(entry_timeframe_lows[i:i+forecast_period+1])
        # possible lowest percentage
        downside_percentage_change = ((lowest_price_in_the_next_forecast_period - entry_timeframe_close) / entry_timeframe_close) * 100 # ((b - a) / a) * 100
        
        # possible highest price
        highest_price_in_the_next_forecast_period = np.max(entry_timeframe_highs[i:i+forecast_period+1])
        # possible highest percentage
        upside_percentage_change = ((highest_price_in_the_next_forecast_period - entry_timeframe_close) / entry_timeframe_close) * 100 # ((b - a) / a) * 100

        # trade's closing price
        trade_closing_price = entry_timeframe_closes[i:i+forecast_period+1][-1]
        # trade's closing percentage
        trade_closing_percentage = ((trade_closing_price - entry_timeframe_close) / entry_timeframe_close) * 100 # ((b - a) / a) * 100

        # append generated y values to df dict
        y_dict['Max % Down'].append(downside_percentage_change)
        y_dict['Max % Up'].append(upside_percentage_change)
        y_dict["Trade's Session Closing %"].append(trade_closing_percentage)

    # return y features according to y type *************************************************************************************
    if y_type == 'minimum maximum':
        # build pandas dataframe using y_dict *************************************************************************
        y_features_dataframe = pd.DataFrame(y_dict)
        print('\n\nY Features Dataset:\n', y_features_dataframe.head(), '\n\n')
        # *************************************************************************************************************

        # return y_features_dataframe, and y_column_list
        return y_features_dataframe, y_column_list
    elif y_type == 'buy or sell':
        # initialize new y dict
        new_y_dict = {
            'Action': deque([])
        }

        # get y column list ... target variables
        y_column_list = list(new_y_dict.keys())

        # generate new y features
        for i in tqdm(range(len(y_dict['Max % Up'])), desc="Y Feature Engineering Stage 2", unit="row"):
            maximum_upside = y_dict['Max % Up'][i]
            maximum_downside =  y_dict['Max % Down'][i]

            # buy
            if maximum_upside >= reward and maximum_downside > -risk: new_y_dict['Action'].append('Buy')
            # sell
            elif maximum_downside <= -reward and maximum_upside < risk: new_y_dict['Action'].append('Sell')
            # nothing
            else: new_y_dict['Action'].append('Nothing')

        # join y_dict to new_y_dict
        new_y_dict.update(y_dict)

        # build pandas dataframe using new_y_dict *********************************************************************
        y_features_dataframe = pd.DataFrame(new_y_dict)
        print('\n\nY Features Dataset:\n', y_features_dataframe.head(), '\n\n')
        # *************************************************************************************************************

        # return y_features_dataframe, and y_column_list
        return y_features_dataframe, y_column_list
    # ***************************************************************************************************************************