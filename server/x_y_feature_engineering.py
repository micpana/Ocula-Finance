from data_acquisition import acquire_data
from x_feature_engineering import engineer_x
from y_feature_engineering import engineer_y
import pandas as pd
from settings import remove_last_n_values_without_full_forecast
from symbol_config import get_symbol_config

def engineer_x_y(symbol, y_type, call_module): # call module = training / prediction
    # list of timeframes ... in descending order ... M15 has to be the entry timeframe, certain configurations are currently causing that limit
    timeframes = [
        'Daily', 
        'H4', 
        'H1', 
        # 'M30',
        'M15'
    ]

    # entry timeframe ... smallest timeframe on the list, ie last timeframe since the list is sorted in descending order
    entry_timeframe = timeframes[-1]

    # timeframes and their minutes in a single bar
    timeframes_and_their_minutes_in_a_single_bar = {
        'Daily': 1440, 
        'H4': 240, 
        'H1': 60, 
        'M30': 30,
        'M15': 15
    }

    # entry timeframe minutes in a single bar
    entry_timeframe_minutes_in_a_single_bar = timeframes_and_their_minutes_in_a_single_bar[entry_timeframe]

    # get every timeframe's ohlc data as data dict
    ohlc_data_dict = acquire_data(symbol, timeframes, call_module)

    # get x_features_dataframe
    x_features_dataframe, x_column_list = engineer_x(ohlc_data_dict, timeframes, entry_timeframe)

    # if call module = training
    if call_module == 'training':
        # get y_features_dataframe
        y_features_dataframe, y_column_list = engineer_y(x_features_dataframe, y_type, entry_timeframe, symbol)

        # combine x and y feature dataframes
        x_y_features_dataframe = pd.concat([x_features_dataframe, y_features_dataframe], axis=1)

        # get symbol data *********************************************************************************************
        # get symbol config
        symbol_config = get_symbol_config(symbol)
        
        # forecast period
        forecast_period = symbol_config['forecast_period']
        # *************************************************************************************************************

        # if set to remove last n(forecast period) values without full forecast
        if remove_last_n_values_without_full_forecast() == True:
            x_y_features_dataframe = x_y_features_dataframe.iloc[:-forecast_period]

        # return x_y_features_dataframe
        return x_y_features_dataframe, x_column_list, y_column_list, entry_timeframe, timeframes

    # if call module = prediction
    if call_module == 'prediction':
        # return x_features_dataframe
        return x_features_dataframe, x_column_list, entry_timeframe, timeframes, entry_timeframe_minutes_in_a_single_bar