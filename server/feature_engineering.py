import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import deque
from datetime import datetime
from settings import get_lookback_period, get_forecast_period, x_use_percentages, y_use_percentages, get_entry_timeframe, use_weighted_features, x_use_log_returns, use_price_action_features
from price_action_features import extract_price_action_features

# get dataset with engineered featured
def get_feature_dataset(timeframes, timeframe_1_ohlc_df, timeframe_2_ohlc_df, timeframe_3_ohlc_df, timeframe_4_ohlc_df, timeframe_5_ohlc_df, timeframe_6_ohlc_df, timeframe_7_ohlc_df, timeframe_8_ohlc_df, closing_prices_only_status):
    # get closes and dates
    if len(timeframes) >= 1: timeframe_1_dates = timeframe_1_ohlc_df['time'].values
    if len(timeframes) >= 1: timeframe_1_closes = timeframe_1_ohlc_df['close'].values
    if len(timeframes) >= 2: timeframe_2_dates = timeframe_2_ohlc_df['time'].values
    if len(timeframes) >= 2: timeframe_2_closes = timeframe_2_ohlc_df['close'].values
    if len(timeframes) >= 3: timeframe_3_dates = timeframe_3_ohlc_df['time'].values
    if len(timeframes) >= 3: timeframe_3_closes = timeframe_3_ohlc_df['close'].values
    if len(timeframes) >= 4: timeframe_4_dates = timeframe_4_ohlc_df['time'].values
    if len(timeframes) >= 4: timeframe_4_closes = timeframe_4_ohlc_df['close'].values
    if len(timeframes) >= 5: timeframe_5_dates = timeframe_5_ohlc_df['time'].values
    if len(timeframes) >= 5: timeframe_5_closes = timeframe_5_ohlc_df['close'].values
    if len(timeframes) >= 6: timeframe_6_dates = timeframe_6_ohlc_df['time'].values
    if len(timeframes) >= 6: timeframe_6_closes = timeframe_6_ohlc_df['close'].values
    if len(timeframes) >= 7: timeframe_7_dates = timeframe_7_ohlc_df['time'].values
    if len(timeframes) >= 7: timeframe_7_closes = timeframe_7_ohlc_df['close'].values
    if len(timeframes) >= 8: timeframe_8_dates = timeframe_8_ohlc_df['time'].values
    if len(timeframes) >= 8: timeframe_8_closes = timeframe_8_ohlc_df['close'].values

    # if set to use all ohlc data or set to use weighted features or set to use price action features, get additional ohlc data thats missing above
    if closing_prices_only_status == False or use_weighted_features() == True or use_price_action_features() == True: 
        if len(timeframes) >= 1: timeframe_1_opens = timeframe_1_ohlc_df['open'].values
        if len(timeframes) >= 1: timeframe_1_highs = timeframe_1_ohlc_df['high'].values
        if len(timeframes) >= 1: timeframe_1_lows = timeframe_1_ohlc_df['low'].values
        if len(timeframes) >= 2: timeframe_2_opens = timeframe_2_ohlc_df['open'].values
        if len(timeframes) >= 2: timeframe_2_highs = timeframe_2_ohlc_df['high'].values
        if len(timeframes) >= 2: timeframe_2_lows = timeframe_2_ohlc_df['low'].values
        if len(timeframes) >= 3: timeframe_3_opens = timeframe_3_ohlc_df['open'].values
        if len(timeframes) >= 3: timeframe_3_highs = timeframe_3_ohlc_df['high'].values
        if len(timeframes) >= 3: timeframe_3_lows = timeframe_3_ohlc_df['low'].values
        if len(timeframes) >= 4: timeframe_4_opens = timeframe_4_ohlc_df['open'].values
        if len(timeframes) >= 4: timeframe_4_highs = timeframe_4_ohlc_df['high'].values
        if len(timeframes) >= 4: timeframe_4_lows = timeframe_4_ohlc_df['low'].values
        if len(timeframes) >= 5: timeframe_5_opens = timeframe_5_ohlc_df['open'].values
        if len(timeframes) >= 5: timeframe_5_highs = timeframe_5_ohlc_df['high'].values
        if len(timeframes) >= 5: timeframe_5_lows = timeframe_5_ohlc_df['low'].values
        if len(timeframes) >= 6: timeframe_6_opens = timeframe_6_ohlc_df['open'].values
        if len(timeframes) >= 6: timeframe_6_highs = timeframe_6_ohlc_df['high'].values
        if len(timeframes) >= 6: timeframe_6_lows = timeframe_6_ohlc_df['low'].values
        if len(timeframes) >= 7: timeframe_7_opens = timeframe_7_ohlc_df['open'].values
        if len(timeframes) >= 7: timeframe_7_highs = timeframe_7_ohlc_df['high'].values
        if len(timeframes) >= 7: timeframe_7_lows = timeframe_7_ohlc_df['low'].values
        if len(timeframes) >= 8: timeframe_8_opens = timeframe_8_ohlc_df['open'].values
        if len(timeframes) >= 8: timeframe_8_highs = timeframe_8_ohlc_df['high'].values
        if len(timeframes) >= 8: timeframe_8_lows = timeframe_8_ohlc_df['low'].values

    # get entry timeframe
    entry_timeframe = get_entry_timeframe()
    
    # get entry timeframe data ... dates, highs, lows
    entry_timeframe_number = timeframes.index(entry_timeframe) + 1
    if entry_timeframe_number == 1:
        entry_timeframe_dates = timeframe_1_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_1_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_1_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_1_ohlc_df['close'].values
    if entry_timeframe_number == 2:
        entry_timeframe_dates = timeframe_2_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_2_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_2_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_2_ohlc_df['close'].values
    if entry_timeframe_number == 3:
        entry_timeframe_dates = timeframe_3_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_3_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_3_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_3_ohlc_df['close'].values
    if entry_timeframe_number == 4:
        entry_timeframe_dates = timeframe_4_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_4_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_4_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_4_ohlc_df['close'].values
    if entry_timeframe_number == 5:
        entry_timeframe_dates = timeframe_5_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_5_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_5_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_5_ohlc_df['close'].values
    if entry_timeframe_number == 6:
        entry_timeframe_dates = timeframe_6_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_6_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_6_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_6_ohlc_df['close'].values
    if entry_timeframe_number == 7:
        entry_timeframe_dates = timeframe_7_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_7_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_7_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_7_ohlc_df['close'].values
    if entry_timeframe_number == 8:
        entry_timeframe_dates = timeframe_8_ohlc_df['time'].values
        entry_timeframe_highs = timeframe_8_ohlc_df['high'].values
        entry_timeframe_lows = timeframe_8_ohlc_df['low'].values
        entry_timeframe_closes = timeframe_8_ohlc_df['close'].values
        
    # if use_price_action_features is set to false, and x use percentages is set to true and use_weighted_features is set to false, turn prices to percentage changes in price
    if use_price_action_features() == False and x_use_percentages() == True and use_weighted_features() == False:
        # if set to use log returns 
        if x_use_log_returns() == True:
            # turn closing prices to percentage changes in price
            if len(timeframes) >= 1: timeframe_1_closes_percentages = np.log(timeframe_1_closes / np.roll(timeframe_1_closes, 1))[1:]
            if len(timeframes) >= 2: timeframe_2_closes_percentages = np.log(timeframe_2_closes / np.roll(timeframe_2_closes, 1))[1:]
            if len(timeframes) >= 3: timeframe_3_closes_percentages = np.log(timeframe_3_closes / np.roll(timeframe_3_closes, 1))[1:]
            if len(timeframes) >= 4: timeframe_4_closes_percentages = np.log(timeframe_4_closes / np.roll(timeframe_4_closes, 1))[1:]
            if len(timeframes) >= 5: timeframe_5_closes_percentages = np.log(timeframe_5_closes / np.roll(timeframe_5_closes, 1))[1:]
            if len(timeframes) >= 6: timeframe_6_closes_percentages = np.log(timeframe_6_closes / np.roll(timeframe_6_closes, 1))[1:]
            if len(timeframes) >= 7: timeframe_7_closes_percentages = np.log(timeframe_7_closes / np.roll(timeframe_7_closes, 1))[1:]
            if len(timeframes) >= 8: timeframe_8_closes_percentages = np.log(timeframe_8_closes / np.roll(timeframe_8_closes, 1))[1:]

            # if set to use all ohlc data, turn the rest of the ohlc prices to percentage changes in price
            if closing_prices_only_status == False: 
                # turn opening prices to percentage changes in price
                if len(timeframes) >= 1: timeframe_1_opens_percentages = np.log(timeframe_1_opens / np.roll(timeframe_1_opens, 1))[1:]
                if len(timeframes) >= 2: timeframe_2_opens_percentages = np.log(timeframe_2_opens / np.roll(timeframe_2_opens, 1))[1:]
                if len(timeframes) >= 3: timeframe_3_opens_percentages = np.log(timeframe_3_opens / np.roll(timeframe_3_opens, 1))[1:]
                if len(timeframes) >= 4: timeframe_4_opens_percentages = np.log(timeframe_4_opens / np.roll(timeframe_4_opens, 1))[1:]
                if len(timeframes) >= 5: timeframe_5_opens_percentages = np.log(timeframe_5_opens / np.roll(timeframe_5_opens, 1))[1:]
                if len(timeframes) >= 6: timeframe_6_opens_percentages = np.log(timeframe_6_opens / np.roll(timeframe_6_opens, 1))[1:]
                if len(timeframes) >= 7: timeframe_7_opens_percentages = np.log(timeframe_7_opens / np.roll(timeframe_7_opens, 1))[1:]
                if len(timeframes) >= 8: timeframe_8_opens_percentages = np.log(timeframe_8_opens / np.roll(timeframe_8_opens, 1))[1:]

                # turn high prices to percentage changes in price
                if len(timeframes) >= 1: timeframe_1_highs_percentages = np.log(timeframe_1_highs / np.roll(timeframe_1_highs, 1))[1:]
                if len(timeframes) >= 2: timeframe_2_highs_percentages = np.log(timeframe_2_highs / np.roll(timeframe_2_highs, 1))[1:]
                if len(timeframes) >= 3: timeframe_3_highs_percentages = np.log(timeframe_3_highs / np.roll(timeframe_3_highs, 1))[1:]
                if len(timeframes) >= 4: timeframe_4_highs_percentages = np.log(timeframe_4_highs / np.roll(timeframe_4_highs, 1))[1:]
                if len(timeframes) >= 5: timeframe_5_highs_percentages = np.log(timeframe_5_highs / np.roll(timeframe_5_highs, 1))[1:]
                if len(timeframes) >= 6: timeframe_6_highs_percentages = np.log(timeframe_6_highs / np.roll(timeframe_6_highs, 1))[1:]
                if len(timeframes) >= 7: timeframe_7_highs_percentages = np.log(timeframe_7_highs / np.roll(timeframe_7_highs, 1))[1:]
                if len(timeframes) >= 8: timeframe_8_highs_percentages = np.log(timeframe_8_highs / np.roll(timeframe_8_highs, 1))[1:]

                # turn low prices to percentage changes in price
                if len(timeframes) >= 1: timeframe_1_lows_percentages = np.log(timeframe_1_lows / np.roll(timeframe_1_lows, 1))[1:]
                if len(timeframes) >= 2: timeframe_2_lows_percentages = np.log(timeframe_2_lows / np.roll(timeframe_2_lows, 1))[1:]
                if len(timeframes) >= 3: timeframe_3_lows_percentages = np.log(timeframe_3_lows / np.roll(timeframe_3_lows, 1))[1:]
                if len(timeframes) >= 4: timeframe_4_lows_percentages = np.log(timeframe_4_lows / np.roll(timeframe_4_lows, 1))[1:]
                if len(timeframes) >= 5: timeframe_5_lows_percentages = np.log(timeframe_5_lows / np.roll(timeframe_5_lows, 1))[1:]
                if len(timeframes) >= 6: timeframe_6_lows_percentages = np.log(timeframe_6_lows / np.roll(timeframe_6_lows, 1))[1:]
                if len(timeframes) >= 7: timeframe_7_lows_percentages = np.log(timeframe_7_lows / np.roll(timeframe_7_lows, 1))[1:]
                if len(timeframes) >= 8: timeframe_8_lows_percentages = np.log(timeframe_8_lows / np.roll(timeframe_8_lows, 1))[1:]

        # if set to use normal returns
        else:
            # turn closing prices to percentage changes in price
            if len(timeframes) >= 1: timeframe_1_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_1_closes[1:], timeframe_1_closes)], dtype=float)
            if len(timeframes) >= 2: timeframe_2_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_2_closes[1:], timeframe_2_closes)], dtype=float)
            if len(timeframes) >= 3: timeframe_3_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_3_closes[1:], timeframe_3_closes)], dtype=float)
            if len(timeframes) >= 4: timeframe_4_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_4_closes[1:], timeframe_4_closes)], dtype=float)
            if len(timeframes) >= 5: timeframe_5_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_5_closes[1:], timeframe_5_closes)], dtype=float)
            if len(timeframes) >= 6: timeframe_6_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_6_closes[1:], timeframe_6_closes)], dtype=float)
            if len(timeframes) >= 7: timeframe_7_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_7_closes[1:], timeframe_7_closes)], dtype=float)
            if len(timeframes) >= 8: timeframe_8_closes_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_8_closes[1:], timeframe_8_closes)], dtype=float)

            # if set to use all ohlc data, turn the rest of the ohlc prices to percentage changes in price
            if closing_prices_only_status == False: 
                # turn opening prices to percentage changes in price
                if len(timeframes) >= 1: timeframe_1_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_1_opens[1:], timeframe_1_opens)], dtype=float)
                if len(timeframes) >= 2: timeframe_2_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_2_opens[1:], timeframe_2_opens)], dtype=float)
                if len(timeframes) >= 3: timeframe_3_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_3_opens[1:], timeframe_3_opens)], dtype=float)
                if len(timeframes) >= 4: timeframe_4_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_4_opens[1:], timeframe_4_opens)], dtype=float)
                if len(timeframes) >= 5: timeframe_5_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_5_opens[1:], timeframe_5_opens)], dtype=float)
                if len(timeframes) >= 6: timeframe_6_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_6_opens[1:], timeframe_6_opens)], dtype=float)
                if len(timeframes) >= 7: timeframe_7_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_7_opens[1:], timeframe_7_opens)], dtype=float)
                if len(timeframes) >= 8: timeframe_8_opens_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_8_opens[1:], timeframe_8_opens)], dtype=float)

                # turn high prices to percentage changes in price
                if len(timeframes) >= 1: timeframe_1_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_1_highs[1:], timeframe_1_highs)], dtype=float)
                if len(timeframes) >= 2: timeframe_2_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_2_highs[1:], timeframe_2_highs)], dtype=float)
                if len(timeframes) >= 3: timeframe_3_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_3_highs[1:], timeframe_3_highs)], dtype=float)
                if len(timeframes) >= 4: timeframe_4_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_4_highs[1:], timeframe_4_highs)], dtype=float)
                if len(timeframes) >= 5: timeframe_5_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_5_highs[1:], timeframe_5_highs)], dtype=float)
                if len(timeframes) >= 6: timeframe_6_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_6_highs[1:], timeframe_6_highs)], dtype=float)
                if len(timeframes) >= 7: timeframe_7_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_7_highs[1:], timeframe_7_highs)], dtype=float)
                if len(timeframes) >= 8: timeframe_8_highs_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_8_highs[1:], timeframe_8_highs)], dtype=float)

                # turn low prices to percentage changes in price
                if len(timeframes) >= 1: timeframe_1_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_1_lows[1:], timeframe_1_lows)], dtype=float)
                if len(timeframes) >= 2: timeframe_2_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_2_lows[1:], timeframe_2_lows)], dtype=float)
                if len(timeframes) >= 3: timeframe_3_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_3_lows[1:], timeframe_3_lows)], dtype=float)
                if len(timeframes) >= 4: timeframe_4_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_4_lows[1:], timeframe_4_lows)], dtype=float)
                if len(timeframes) >= 5: timeframe_5_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_5_lows[1:], timeframe_5_lows)], dtype=float)
                if len(timeframes) >= 6: timeframe_6_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_6_lows[1:], timeframe_6_lows)], dtype=float)
                if len(timeframes) >= 7: timeframe_7_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_7_lows[1:], timeframe_7_lows)], dtype=float)
                if len(timeframes) >= 8: timeframe_8_lows_percentages = np.array([100.0 * a1 / a2 - 100 for a1, a2 in zip(timeframe_8_lows[1:], timeframe_8_lows)], dtype=float)

        # make sure dates match percentages... first close value was only used for calculating the first percentage then discarded, so first date in each list must be discarded as well
        if len(timeframes) >= 1: timeframe_1_dates = np.array(timeframe_1_dates[1:], dtype=str)
        if len(timeframes) >= 2: timeframe_2_dates = np.array(timeframe_2_dates[1:], dtype=str)
        if len(timeframes) >= 3: timeframe_3_dates = np.array(timeframe_3_dates[1:], dtype=str)
        if len(timeframes) >= 4: timeframe_4_dates = np.array(timeframe_4_dates[1:], dtype=str)
        if len(timeframes) >= 5: timeframe_5_dates = np.array(timeframe_5_dates[1:], dtype=str)
        if len(timeframes) >= 6: timeframe_6_dates = np.array(timeframe_6_dates[1:], dtype=str)
        if len(timeframes) >= 7: timeframe_7_dates = np.array(timeframe_7_dates[1:], dtype=str)
        if len(timeframes) >= 8: timeframe_8_dates = np.array(timeframe_8_dates[1:], dtype=str)

        # make sure entry timeframe data matches percentages as well
        entry_timeframe_dates = np.array(entry_timeframe_dates[1:], dtype=str)
        entry_timeframe_highs = np.array(entry_timeframe_highs[1:], dtype=float)
        entry_timeframe_lows = np.array(entry_timeframe_lows[1:], dtype=float)
        entry_timeframe_closes = np.array(entry_timeframe_closes[1:], dtype=float)

    # metrics *************************************************************************************************************************
    # all
    lookback = get_lookback_period()
    forecast = get_forecast_period()
    # raw price or percentage features
    x_opens_column_name_mid_section = '_Open_'
    x_highs_column_name_mid_section = '_High_'
    x_lows_column_name_mid_section = '_Low_'
    x_closes_column_name_mid_section = '_Close_'
    # weight features
    x_weighted_features_column_name_mid_section = '_Candle_'
    # price action features
    x_price_action_features_column_1_mid_section = '_Structure_Value_1_'
    x_price_action_features_column_2_mid_section = '_Structure_Value_2_'
    x_price_action_features_column_3_mid_section = '_Structure_Value_3_'
    x_price_action_features_column_4_mid_section = '_Gradient_1_'
    x_price_action_features_column_5_mid_section = '_Gradient_2_'
    x_price_action_features_column_6_mid_section = '_Last_Close_'
    # output features
    y_column_1 = 'Maximum_Possible_Down_Move'
    y_column_2 = 'Maximum_Possible_Up_Move'

    # determine row data loops ... useful for loopback range data fill, for non market structure features
    if use_price_action_features() == True:
        row_data_loops = 1
    else:
        row_data_loops = lookback

    # initialize df dict
    df_dict = {}
    for timeframe in timeframes:
        for i in range(row_data_loops):
            # if set to use price action features
            if use_price_action_features() == True:
                price_action_features_column_1_name = timeframe + x_price_action_features_column_1_mid_section + str(i+1)
                df_dict[price_action_features_column_1_name] = deque([])
                price_action_features_column_2_name = timeframe + x_price_action_features_column_2_mid_section + str(i+1)
                df_dict[price_action_features_column_2_name] = deque([])
                price_action_features_column_3_name = timeframe + x_price_action_features_column_3_mid_section + str(i+1)
                df_dict[price_action_features_column_3_name] = deque([])
                price_action_features_column_4_name = timeframe + x_price_action_features_column_4_mid_section + str(i+1)
                df_dict[price_action_features_column_4_name] = deque([])
                price_action_features_column_5_name = timeframe + x_price_action_features_column_5_mid_section + str(i+1)
                df_dict[price_action_features_column_5_name] = deque([])
                price_action_features_column_6_name = timeframe + x_price_action_features_column_6_mid_section + str(i+1)
                df_dict[price_action_features_column_6_name] = deque([])
            else:
                # if set to use weighted features
                if use_weighted_features() == True:
                    # timeframe's column for weighted features
                    weighted_features_column_name = timeframe + x_weighted_features_column_name_mid_section + str(i+1)
                    df_dict[weighted_features_column_name] = deque([])
                else:
                    # if set to use all ohlc data, create columns for all ohl data as well ... ohlc order is crucial
                    if closing_prices_only_status == False: 
                        # timeframe's column for opening prices
                        opens_column_name = timeframe + x_opens_column_name_mid_section + str(i+1)
                        df_dict[opens_column_name] = deque([])
                        # timeframe's column for highs prices
                        highs_column_name = timeframe + x_highs_column_name_mid_section + str(i+1)
                        df_dict[highs_column_name] = deque([])
                        # timeframe's column for lows prices
                        lows_column_name = timeframe + x_lows_column_name_mid_section + str(i+1)
                        df_dict[lows_column_name] = deque([])
                    # timeframe's column for closing prices
                    closes_column_name = timeframe + x_closes_column_name_mid_section + str(i+1)
                    df_dict[closes_column_name] = deque([])
    
    # list of all x columns
    x_column_list = list(df_dict.keys())

    # initialize y columns
    df_dict[y_column_1] = deque([])
    df_dict[y_column_2] = deque([])

    # determine loop starting point
    if entry_timeframe_number == len(timeframes): # entry timeframe is the smallest timeframe
        loop_starting_index = lookback
    else: # entry timeframe is not the smallest timeframe
        # get the most recent first date found on other timeframes ... take into account the lookback period
        if len(timeframes) >= 1: most_recent_first_date_found = timeframe_1_dates[0]
        if len(timeframes) >= 2: 
            if timeframe_2_dates[lookback:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_2_dates[lookback:][0]
        if len(timeframes) >= 3: 
            if timeframe_3_dates[lookback:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_3_dates[lookback:][0]
        if len(timeframes) >= 4: 
            if timeframe_4_dates[lookback:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_4_dates[lookback:][0]
        if len(timeframes) >= 5: 
            if timeframe_5_dates[lookback:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_5_dates[lookback:][0]
        if len(timeframes) >= 6: 
            if timeframe_6_dates[lookback:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_6_dates[lookback:][0]
        if len(timeframes) >= 7: 
            if timeframe_7_dates[lookback:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_7_dates[lookback:][0]
        if len(timeframes) >= 8: 
            if timeframe_8_dates[lookback:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_8_dates[lookback:][0]
        # get most recent first date's index in the entry timeframe's data starting from the lookback point
        smallest_timeframe_date_index_in_entry_timeframe_data = np.where(entry_timeframe_dates[lookback:] >= most_recent_first_date_found)[0][0]
        # start looping at the most recent first date's index in the entry timeframe's data ... add lookback to the index for index to match main df since we started looking at lookback
        loop_starting_index = smallest_timeframe_date_index_in_entry_timeframe_data + lookback
        print("\n\nThe most recent first date found", most_recent_first_date_found, "was found on index", loop_starting_index, "of the entry timeframe's data. Looping will start there.")

    # populate df dict
    for i in tqdm(range(loop_starting_index, len(entry_timeframe_closes), +1), desc="Feature Engineering", unit="row"): # using entry timeframe closes
        # entry timeframe date
        entry_timeframe_date = entry_timeframe_dates[i]

        # markers for duplicate index's value avoidance on each row
        timeframe_1_last_index = None
        timeframe_2_last_index = None
        timeframe_3_last_index = None
        timeframe_4_last_index = None
        timeframe_5_last_index = None
        timeframe_6_last_index = None
        timeframe_7_last_index = None
        timeframe_8_last_index = None

        # generate current row data by lookback *****
        for j in range(row_data_loops):
            # check if the entry timeframe date is available in the other timeframe data ... the data before and during the date should have >= the same length as the given lookback period ... if these conditions are not met, skip row
            try:
                if len(timeframes) >= 1: 
                    # duplication on same row avoidance, we just want the last n (lookback period) values as they are in the series
                    if timeframe_1_last_index == None: 
                        timeframe_1_index_of_date_reference = np.where(timeframe_1_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_1_index_of_date_reference = timeframe_1_last_index + 1

                if len(timeframes) >= 2: 
                    # duplication on same row avoidance, we just want the last n values as they are in the series
                    if timeframe_2_last_index == None: 
                        timeframe_2_index_of_date_reference = np.where(timeframe_2_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_2_index_of_date_reference = timeframe_2_last_index + 1

                if len(timeframes) >= 3: 
                    # duplication on same row avoidance, we just want the last n values as they are in the series
                    if timeframe_3_last_index == None: 
                        timeframe_3_index_of_date_reference = np.where(timeframe_3_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_3_index_of_date_reference = timeframe_3_last_index + 1
                
                if len(timeframes) >= 4: 
                    # duplication on same row avoidance, we just want the last n values as they are in the series
                    if timeframe_4_last_index == None: 
                        timeframe_4_index_of_date_reference = np.where(timeframe_4_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_4_index_of_date_reference = timeframe_4_last_index + 1
                
                if len(timeframes) >= 5: 
                    # duplication on same row avoidance, we just want the last n values as they are in the series
                    if timeframe_5_last_index == None: 
                        timeframe_5_index_of_date_reference = np.where(timeframe_5_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_5_index_of_date_reference = timeframe_5_last_index + 1
                
                if len(timeframes) >= 6: 
                    # duplication on same row avoidance, we just want the last n values as they are in the series
                    if timeframe_6_last_index == None: 
                        timeframe_6_index_of_date_reference = np.where(timeframe_6_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_6_index_of_date_reference = timeframe_6_last_index + 1
                
                if len(timeframes) >= 7: 
                    # duplication on same row avoidance, we just want the last n values as they are in the series
                    if timeframe_7_last_index == None: 
                        timeframe_7_index_of_date_reference = np.where(timeframe_7_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_7_index_of_date_reference = timeframe_7_last_index + 1
                    
                if len(timeframes) >= 8: 
                    # duplication on same row avoidance, we just want the last n values as they are in the series
                    if timeframe_8_last_index == None: 
                        timeframe_8_index_of_date_reference = np.where(timeframe_8_dates <= entry_timeframe_date)[0][-1]
                    else:
                        timeframe_8_index_of_date_reference = timeframe_8_last_index + 1

                # compare indexes to required lookback data ... for logging timeframes with indexes outside range
                timeframes_outside_range = ''
                if len(timeframes) >= 1:
                    if timeframe_1_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 1'
                if len(timeframes) >= 2:
                    if timeframe_2_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 2'
                if len(timeframes) >= 3:
                    if timeframe_3_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 3'
                if len(timeframes) >= 4:
                    if timeframe_4_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 4'
                if len(timeframes) >= 5:
                    if timeframe_5_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 5'
                if len(timeframes) >= 6:
                    if timeframe_6_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 6'
                if len(timeframes) >= 7:
                    if timeframe_7_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 7'
                if len(timeframes) >= 8:
                    if timeframe_8_index_of_date_reference - lookback < 0:
                        timeframes_outside_range = timeframes_outside_range + ' Timeframe 8'
                if timeframes_outside_range != '':
                    print("Current entry timeframe's date", entry_timeframe_date, "is not within date ranges of the following timeframes:", timeframes_outside_range, ", as per available data and set lookback")
                    print('At index', i, 'of', len(entry_timeframe_closes))
                    break

            except Exception as e:
                print("Current entry timeframe's date", entry_timeframe_date, "is not within one or more of the other timeframes' date ranges as per available data and set lookback")
                print(e, 'at index', i, 'of', len(entry_timeframe_closes))
                break

            # generate current row data by timeframe *****
            for timeframe in timeframes:
                # if set to use price action features
                if use_price_action_features() == True:
                    price_action_features_column_1_name = timeframe + x_price_action_features_column_1_mid_section + str(j+1)
                    price_action_features_column_2_name = timeframe + x_price_action_features_column_2_mid_section + str(j+1)
                    price_action_features_column_3_name = timeframe + x_price_action_features_column_3_mid_section + str(j+1)
                    price_action_features_column_4_name = timeframe + x_price_action_features_column_4_mid_section + str(j+1)
                    price_action_features_column_5_name = timeframe + x_price_action_features_column_5_mid_section + str(j+1)
                    price_action_features_column_6_name = timeframe + x_price_action_features_column_6_mid_section + str(j+1)
                else:
                    # if set to use weighted features
                    if use_weighted_features() == True:
                        # timeframe's column for weighted features
                        weighted_features_column_name = timeframe + x_weighted_features_column_name_mid_section + str(j+1) # timeframe's column name for weighted features
                    else:
                        # if set to use all ohlc data, state columns for all ohl data as well
                        if closing_prices_only_status == False: 
                            opens_column_name = timeframe + x_opens_column_name_mid_section + str(j+1) # timeframe's column name for opening prices
                            highs_column_name = timeframe + x_highs_column_name_mid_section + str(j+1) # timeframe's column name for highs prices
                            lows_column_name = timeframe + x_lows_column_name_mid_section + str(j+1) # timeframe's column name for lows prices
                        closes_column_name = timeframe + x_closes_column_name_mid_section + str(j+1) # timeframe's column name for closing prices

                # get current timeframe's number
                timeframe_number = timeframes.index(timeframe) + 1

                # function for weighted features
                def extract_weighted_features(candle_open, candle_high, candle_low, candle_close):
                    # for bullish candle
                    if candle_close >= candle_open:
                        if x_use_percentages() == True: # percentages
                            # pushes
                            sellers_wick = ((candle_high - candle_close) / candle_close) * 100 # ((b - a) / a) * 100
                            buyers_body = ((candle_close - candle_open) / candle_open) * 100 # ((b - a) / a) * 100
                            buyers_wick = ((candle_open - candle_low) / candle_low) * 100 # ((b - a) / a) * 100

                        else: # price
                            # pushes
                            sellers_wick = candle_high - candle_close
                            buyers_body = candle_close - candle_open
                            buyers_wick = candle_open - candle_low

                        # candle's weighted value
                        weighted_value = buyers_body + buyers_wick - sellers_wick

                    # for bearish candle
                    else:
                        if x_use_percentages() == True: # percentages
                            # pushes
                            sellers_wick = ((candle_high - candle_open) / candle_open) * 100 # ((b - a) / a) * 100
                            sellers_body = ((candle_open - candle_close) / candle_close) * 100 # ((b - a) / a) * 100
                            buyers_wick = ((candle_close - candle_low) / candle_low) * 100 # ((b - a) / a) * 100
                            
                        else: # price
                            # pushes
                            sellers_wick = candle_high - candle_open
                            sellers_body = candle_open - candle_close
                            buyers_wick = candle_close - candle_low

                        # candle's weighted value
                        weighted_value = buyers_wick - sellers_body - sellers_wick

                    # return candle's weighted value
                    return weighted_value

                # populate data by timeframe
                if timeframe_number == 1:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_1_last_index = timeframe_1_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_1_lows[timeframe_1_index_of_date_reference-lookback:timeframe_1_index_of_date_reference+1], 
                            timeframe_1_highs[timeframe_1_index_of_date_reference-lookback:timeframe_1_index_of_date_reference+1], 
                            timeframe_1_closes[timeframe_1_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_1_opens[timeframe_1_index_of_date_reference-lookback]
                            candle_high = timeframe_1_highs[timeframe_1_index_of_date_reference-lookback]
                            candle_low = timeframe_1_lows[timeframe_1_index_of_date_reference-lookback]
                            candle_close = timeframe_1_closes[timeframe_1_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_1_opens_percentages[timeframe_1_index_of_date_reference-lookback]
                                    highs_value = timeframe_1_highs_percentages[timeframe_1_index_of_date_reference-lookback]
                                    lows_value = timeframe_1_lows_percentages[timeframe_1_index_of_date_reference-lookback]
                                closes_value = timeframe_1_closes_percentages[timeframe_1_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_1_opens[timeframe_1_index_of_date_reference-lookback]
                                    highs_value = timeframe_1_highs[timeframe_1_index_of_date_reference-lookback]
                                    lows_value = timeframe_1_lows[timeframe_1_index_of_date_reference-lookback]
                                closes_value = timeframe_1_closes[timeframe_1_index_of_date_reference-lookback]
                    
                elif timeframe_number == 2:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_2_last_index = timeframe_2_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_2_lows[timeframe_2_index_of_date_reference-lookback:timeframe_2_index_of_date_reference+1], 
                            timeframe_2_highs[timeframe_2_index_of_date_reference-lookback:timeframe_2_index_of_date_reference+1], 
                            timeframe_2_closes[timeframe_2_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_2_opens[timeframe_2_index_of_date_reference-lookback]
                            candle_high = timeframe_2_highs[timeframe_2_index_of_date_reference-lookback]
                            candle_low = timeframe_2_lows[timeframe_2_index_of_date_reference-lookback]
                            candle_close = timeframe_2_closes[timeframe_2_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_2_opens_percentages[timeframe_2_index_of_date_reference-lookback]
                                    highs_value = timeframe_2_highs_percentages[timeframe_2_index_of_date_reference-lookback]
                                    lows_value = timeframe_2_lows_percentages[timeframe_2_index_of_date_reference-lookback]
                                closes_value = timeframe_2_closes_percentages[timeframe_2_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_2_opens[timeframe_2_index_of_date_reference-lookback]
                                    highs_value = timeframe_2_highs[timeframe_2_index_of_date_reference-lookback]
                                    lows_value = timeframe_2_lows[timeframe_2_index_of_date_reference-lookback]
                                closes_value = timeframe_2_closes[timeframe_2_index_of_date_reference-lookback]

                elif timeframe_number == 3:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_3_last_index = timeframe_3_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_3_lows[timeframe_3_index_of_date_reference-lookback:timeframe_3_index_of_date_reference+1], 
                            timeframe_3_highs[timeframe_3_index_of_date_reference-lookback:timeframe_3_index_of_date_reference+1], 
                            timeframe_3_closes[timeframe_3_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_3_opens[timeframe_3_index_of_date_reference-lookback]
                            candle_high = timeframe_3_highs[timeframe_3_index_of_date_reference-lookback]
                            candle_low = timeframe_3_lows[timeframe_3_index_of_date_reference-lookback]
                            candle_close = timeframe_3_closes[timeframe_3_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_3_opens_percentages[timeframe_3_index_of_date_reference-lookback]
                                    highs_value = timeframe_3_highs_percentages[timeframe_3_index_of_date_reference-lookback]
                                    lows_value = timeframe_3_lows_percentages[timeframe_3_index_of_date_reference-lookback]
                                closes_value = timeframe_3_closes_percentages[timeframe_3_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_3_opens[timeframe_3_index_of_date_reference-lookback]
                                    highs_value = timeframe_3_highs[timeframe_3_index_of_date_reference-lookback]
                                    lows_value = timeframe_3_lows[timeframe_3_index_of_date_reference-lookback]
                                closes_value = timeframe_3_closes[timeframe_3_index_of_date_reference-lookback]

                elif timeframe_number == 4:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_4_last_index = timeframe_4_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_4_lows[timeframe_4_index_of_date_reference-lookback:timeframe_4_index_of_date_reference+1], 
                            timeframe_4_highs[timeframe_4_index_of_date_reference-lookback:timeframe_4_index_of_date_reference+1], 
                            timeframe_4_closes[timeframe_4_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_4_opens[timeframe_4_index_of_date_reference-lookback]
                            candle_high = timeframe_4_highs[timeframe_4_index_of_date_reference-lookback]
                            candle_low = timeframe_4_lows[timeframe_4_index_of_date_reference-lookback]
                            candle_close = timeframe_4_closes[timeframe_4_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_4_opens_percentages[timeframe_4_index_of_date_reference-lookback]
                                    highs_value = timeframe_4_highs_percentages[timeframe_4_index_of_date_reference-lookback]
                                    lows_value = timeframe_4_lows_percentages[timeframe_4_index_of_date_reference-lookback]
                                closes_value = timeframe_4_closes_percentages[timeframe_4_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_4_opens[timeframe_4_index_of_date_reference-lookback]
                                    highs_value = timeframe_4_highs[timeframe_4_index_of_date_reference-lookback]
                                    lows_value = timeframe_4_lows[timeframe_4_index_of_date_reference-lookback]
                                closes_value = timeframe_4_closes[timeframe_4_index_of_date_reference-lookback]

                elif timeframe_number == 5:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_5_last_index = timeframe_5_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_5_lows[timeframe_5_index_of_date_reference-lookback:timeframe_5_index_of_date_reference+1], 
                            timeframe_5_highs[timeframe_5_index_of_date_reference-lookback:timeframe_5_index_of_date_reference+1], 
                            timeframe_5_closes[timeframe_5_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_5_opens[timeframe_5_index_of_date_reference-lookback]
                            candle_high = timeframe_5_highs[timeframe_5_index_of_date_reference-lookback]
                            candle_low = timeframe_5_lows[timeframe_5_index_of_date_reference-lookback]
                            candle_close = timeframe_5_closes[timeframe_5_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_5_opens_percentages[timeframe_5_index_of_date_reference-lookback]
                                    highs_value = timeframe_5_highs_percentages[timeframe_5_index_of_date_reference-lookback]
                                    lows_value = timeframe_5_lows_percentages[timeframe_5_index_of_date_reference-lookback]
                                closes_value = timeframe_5_closes_percentages[timeframe_5_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_5_opens[timeframe_5_index_of_date_reference-lookback]
                                    highs_value = timeframe_5_highs[timeframe_5_index_of_date_reference-lookback]
                                    lows_value = timeframe_5_lows[timeframe_5_index_of_date_reference-lookback]
                                closes_value = timeframe_5_closes[timeframe_5_index_of_date_reference-lookback]

                elif timeframe_number == 6:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_6_last_index = timeframe_6_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_6_lows[timeframe_6_index_of_date_reference-lookback:timeframe_6_index_of_date_reference+1], 
                            timeframe_6_highs[timeframe_6_index_of_date_reference-lookback:timeframe_6_index_of_date_reference+1], 
                            timeframe_6_closes[timeframe_6_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_6_opens[timeframe_6_index_of_date_reference-lookback]
                            candle_high = timeframe_6_highs[timeframe_6_index_of_date_reference-lookback]
                            candle_low = timeframe_6_lows[timeframe_6_index_of_date_reference-lookback]
                            candle_close = timeframe_6_closes[timeframe_6_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_6_opens_percentages[timeframe_6_index_of_date_reference-lookback]
                                    highs_value = timeframe_6_highs_percentages[timeframe_6_index_of_date_reference-lookback]
                                    lows_value = timeframe_6_lows_percentages[timeframe_6_index_of_date_reference-lookback]
                                closes_value = timeframe_6_closes_percentages[timeframe_6_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_6_opens[timeframe_6_index_of_date_reference-lookback]
                                    highs_value = timeframe_6_highs[timeframe_6_index_of_date_reference-lookback]
                                    lows_value = timeframe_6_lows[timeframe_6_index_of_date_reference-lookback]
                                closes_value = timeframe_6_closes[timeframe_6_index_of_date_reference-lookback]

                elif timeframe_number == 7:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_7_last_index = timeframe_7_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_7_lows[timeframe_7_index_of_date_reference-lookback:timeframe_7_index_of_date_reference+1], 
                            timeframe_7_highs[timeframe_7_index_of_date_reference-lookback:timeframe_7_index_of_date_reference+1], 
                            timeframe_7_closes[timeframe_7_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_7_opens[timeframe_7_index_of_date_reference-lookback]
                            candle_high = timeframe_7_highs[timeframe_7_index_of_date_reference-lookback]
                            candle_low = timeframe_7_lows[timeframe_7_index_of_date_reference-lookback]
                            candle_close = timeframe_7_closes[timeframe_7_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_7_opens_percentages[timeframe_7_index_of_date_reference-lookback]
                                    highs_value = timeframe_7_highs_percentages[timeframe_7_index_of_date_reference-lookback]
                                    lows_value = timeframe_7_lows_percentages[timeframe_7_index_of_date_reference-lookback]
                                closes_value = timeframe_7_closes_percentages[timeframe_7_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_7_opens[timeframe_7_index_of_date_reference-lookback]
                                    highs_value = timeframe_7_highs[timeframe_7_index_of_date_reference-lookback]
                                    lows_value = timeframe_7_lows[timeframe_7_index_of_date_reference-lookback]
                                closes_value = timeframe_7_closes[timeframe_7_index_of_date_reference-lookback]

                elif timeframe_number == 8:
                    # set timeframe's last_index to timeframe's index of date reference
                    timeframe_8_last_index = timeframe_8_index_of_date_reference
                    # if set to use price action features
                    if use_price_action_features() == True:
                        structure_value_1, structure_value_2, structure_value_3, gradient_1, gradient_2, last_close = extract_price_action_features(
                            timeframe_8_lows[timeframe_8_index_of_date_reference-lookback:timeframe_8_index_of_date_reference+1], 
                            timeframe_8_highs[timeframe_8_index_of_date_reference-lookback:timeframe_8_index_of_date_reference+1], 
                            timeframe_8_closes[timeframe_8_index_of_date_reference]
                        )
                    else:
                        # if set to use weighted features
                        if use_weighted_features() == True:
                            # candle data
                            candle_open = timeframe_8_opens[timeframe_8_index_of_date_reference-lookback]
                            candle_high = timeframe_8_highs[timeframe_8_index_of_date_reference-lookback]
                            candle_low = timeframe_8_lows[timeframe_8_index_of_date_reference-lookback]
                            candle_close = timeframe_8_closes[timeframe_8_index_of_date_reference-lookback]
                            # get candle's weighted value
                            weighted_value = extract_weighted_features(candle_open, candle_high, candle_low, candle_close)
                        else:
                            if x_use_percentages() == True: # percentages
                                # if set to use all ohlc data, get price percentage values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_8_opens_percentages[timeframe_8_index_of_date_reference-lookback]
                                    highs_value = timeframe_8_highs_percentages[timeframe_8_index_of_date_reference-lookback]
                                    lows_value = timeframe_8_lows_percentages[timeframe_8_index_of_date_reference-lookback]
                                closes_value = timeframe_8_closes_percentages[timeframe_8_index_of_date_reference-lookback]
                            else: # price
                                # if set to use all ohlc data, get price values for all ohl data as well
                                if closing_prices_only_status == False: 
                                    opens_value = timeframe_8_opens[timeframe_8_index_of_date_reference-lookback]
                                    highs_value = timeframe_8_highs[timeframe_8_index_of_date_reference-lookback]
                                    lows_value = timeframe_8_lows[timeframe_8_index_of_date_reference-lookback]
                                closes_value = timeframe_8_closes[timeframe_8_index_of_date_reference-lookback]

                # append generated x values to df dict *******************************************
                # if set to use price action features
                if use_price_action_features() == True:
                    df_dict[price_action_features_column_1_name].append(structure_value_1) # add column 1 value to df dict
                    df_dict[price_action_features_column_2_name].append(structure_value_2) # add column 2 value to df dict
                    df_dict[price_action_features_column_3_name].append(structure_value_3) # add column 3 value to df dict
                    df_dict[price_action_features_column_4_name].append(gradient_1) # add column 4 value to df dict
                    df_dict[price_action_features_column_5_name].append(gradient_2) # add column 5 value to df dict
                    df_dict[price_action_features_column_6_name].append(last_close) # add column 6 value to df dict
                else:
                    # if set to use weighted features
                    if use_weighted_features() == True:
                        df_dict[weighted_features_column_name].append(weighted_value) # add weighted value to df dict
                    else:
                        # if set to use all ohlc data, add values for all ohl data as well, to the df dict
                        if closing_prices_only_status == False: 
                            df_dict[opens_column_name].append(opens_value) # add opens value to df dict
                            df_dict[highs_column_name].append(highs_value) # add highs value to df dict
                            df_dict[lows_column_name].append(lows_value) # add lows value to df dict
                        df_dict[closes_column_name].append(closes_value) # add closes value to df dict

        # generate y dataframe data *****
        # get entry timeframe's current close
        entry_timeframe_close = entry_timeframe_closes[i]

        # possible lowest price
        lowest_price_in_the_next_forecast_period = np.min(entry_timeframe_lows[i:i+forecast+1])
        downside_percentage_change = ((lowest_price_in_the_next_forecast_period - entry_timeframe_close) / entry_timeframe_close) * 100 # ((b - a) / a) * 100
        
        # possible highest price
        highest_price_in_the_next_forecast_period = np.max(entry_timeframe_highs[i:i+forecast+1])
        upside_percentage_change = ((highest_price_in_the_next_forecast_period - entry_timeframe_close) / entry_timeframe_close) * 100 # ((b - a) / a) * 100

        # append generated y values to df dict
        if y_use_percentages() == True: # percentages
            df_dict[y_column_1].append(downside_percentage_change)
            df_dict[y_column_2].append(upside_percentage_change)
        else: # price
            df_dict[y_column_1].append(lowest_price_in_the_next_forecast_period)
            df_dict[y_column_2].append(highest_price_in_the_next_forecast_period)

    # create dataframe / main dataset
    dataframe = pd.DataFrame(df_dict)

    # get entry timeframe's last datetime
    entry_timeframe_last_datetime = entry_timeframe_dates[-1]

    # return feature dataframe
    return dataframe, x_column_list, y_column_1, y_column_2, entry_timeframe_last_datetime