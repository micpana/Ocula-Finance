from collections import deque
import pandas as pd
import numpy as np
from tqdm import tqdm

def engineer_y(x_features_dataframe, y_type):
    # entry timeframe
    entry_timeframe = 'M15'

    # forecast period
    forecast_period = 7

    # reward ... minimum buy or sell percentage
    reward = 0.15

    # risk 
    risk = reward / 2

    # get entry timeframes high, low, and closing prices
    entry_timeframe_highs = x_features_dataframe[entry_timeframe+'_High'].values
    entry_timeframe_lows = x_features_dataframe[entry_timeframe+'_Low'].values
    entry_timeframe_closes = x_features_dataframe[entry_timeframe+'_Close'].values

    # initialize y features dict
    y_dict = {
        'Max % Down': deque([]),
        'Max % Up': deque([])
    }

    # generate y features
    for i in tqdm(range(len(entry_timeframe_closes)), desc="Y Feature Engineering", unit="row"):
        # get entry timeframe's current close
        entry_timeframe_close = entry_timeframe_closes[i]

        # possible lowest price
        lowest_price_in_the_next_forecast_period = np.min(entry_timeframe_lows[i:i+forecast_period+1])
        downside_percentage_change = ((lowest_price_in_the_next_forecast_period - entry_timeframe_close) / entry_timeframe_close) * 100 # ((b - a) / a) * 100
        
        # possible highest price
        highest_price_in_the_next_forecast_period = np.max(entry_timeframe_highs[i:i+forecast_period+1])
        upside_percentage_change = ((highest_price_in_the_next_forecast_period - entry_timeframe_close) / entry_timeframe_close) * 100 # ((b - a) / a) * 100

        # append generated y values to df dict
        y_dict['Max % Down'].append(downside_percentage_change)
        y_dict['Max % Up'].append(upside_percentage_change)

    # return y features according to y type *************************************************************************************
    if y_type == 'minimum maximum':
        # get y column list
        y_column_list = list(y_dict.keys())

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

        # generate new y features
        for i in tqdm(range(len(y_dict['Max % Up'])), desc="Y Feature Engineering Stage 2", unit="row"):
            maximum_upside = y_dict['Max % Up'][i]
            maximum_downside =  y_dict['Max % Down'][i]

            # buy
            if abs(maximum_upside) >= reward and abs(maximum_downside) < risk: new_y_dict['Action'].append('Buy')
            # sell
            elif abs(maximum_downside) >= reward and abs(maximum_upside) < risk: new_y_dict['Action'].append('Sell')
            # nothing
            else: new_y_dict['Action'].append('Nothing')

        # get y column list
        y_column_list = list(new_y_dict.keys())

        # build pandas dataframe using new_y_dict *********************************************************************
        y_features_dataframe = pd.DataFrame(new_y_dict)
        print('\n\nY Features Dataset:\n', y_features_dataframe.head(), '\n\n')
        # *************************************************************************************************************

        # return y_features_dataframe, and y_column_list
        return y_features_dataframe, y_column_list
    # ***************************************************************************************************************************