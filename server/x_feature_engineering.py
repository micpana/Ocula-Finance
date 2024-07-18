import pandas as pd
import numpy as np
from collections import deque
from tqdm import tqdm

# feature engineering
def engineer_x(daily_df, h4_df, h1_df, m30_df, m15_df):
    # numpy arrays of our data ************************************************************************************************************
    daily_dates = daily_df['time'].values
    daily_opens = daily_df['open'].values
    daily_highs = daily_df['high'].values
    daily_lows = daily_df['low'].values
    daily_closes = daily_df['close'].values
    h4_dates = h4_df['time'].values
    h4_opens = h4_df['open'].values
    h4_highs = h4_df['high'].values
    h4_lows = h4_df['low'].values
    h4_closes = h4_df['close'].values
    h1_dates = h1_df['time'].values
    h1_opens = h1_df['open'].values
    h1_highs = h1_df['high'].values
    h1_lows = h1_df['low'].values
    h1_closes = h1_df['close'].values
    m30_dates = m30_df['time'].values
    m30_opens = m30_df['open'].values
    m30_highs = m30_df['high'].values
    m30_lows = m30_df['low'].values
    m30_closes = m30_df['close'].values
    m15_dates = m15_df['time'].values
    m15_opens = m15_df['open'].values
    m15_highs = m15_df['high'].values
    m15_lows = m15_df['low'].values
    m15_closes = m15_df['close'].values
    # *************************************************************************************************************************************

    # list of timeframes
    timeframes = [
        # 'Daily', 
        # 'H4', 
        'H1', 
        # 'M30',
        'M15'
    ]

    # View Window / Number of candlesticks to look at / Number of candlesticks in viewport
    view_window = 100

    # number of most recent turning points per each view window
    number_of_most_recent_turning_points_per_each_view_window = 3

    # initialize x dict *******************************************************************************************************************
    x_dict = {}
    for timeframe in timeframes:
        # timestamp
        if timeframe == 'M15': x_dict[timeframe+'_Timestamp'] = deque([])
        # ohlc data
        x_dict[timeframe+'_Open'] = deque([])
        x_dict[timeframe+'_High'] = deque([])
        x_dict[timeframe+'_Low'] = deque([])
        x_dict[timeframe+'_Close'] = deque([])
        # ohlc data's log change from first candle in the view window
        x_dict[timeframe+'_Open_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        x_dict[timeframe+'_High_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        x_dict[timeframe+'_Low_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        x_dict[timeframe+'_Close_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        # candlestick types
        x_dict[timeframe+'_Bullish'] = deque([])
        x_dict[timeframe+'_Bearish'] = deque([])
        x_dict[timeframe+'_Doji'] = deque([])
        # wicks
        x_dict[timeframe+'_Upper_Wick'] = deque([])
        x_dict[timeframe+'_Lower_Wick'] = deque([])
        # wicks logs
        x_dict[timeframe+'_Upper_Wick_Log'] = deque([])
        x_dict[timeframe+'_Lower_Wick_Log'] = deque([])
        # body size
        x_dict[timeframe+'_Body_Size'] = deque([])
        # body size log
        x_dict[timeframe+'_Body_Size_Log'] = deque([])
        # candlestick size
        x_dict[timeframe+'_Candlestick_Size'] = deque([])
        # candlestick size log
        x_dict[timeframe+'_Candlestick_Size_Log'] = deque([])
        # 50 MA
        x_dict[timeframe+'_50MA'] = deque([])
        # 50 MA log change from first candle close in view window
        x_dict[timeframe+'_50MA_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        # 25 MA 
        x_dict[timeframe+'_25MA'] = deque([])
        # 25 MA log change from first candle close in view window
        x_dict[timeframe+'_25MA_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        # 10 MA
        x_dict[timeframe+'_10MA'] = deque([])
        # 10 MA log change from first candle close in view window
        x_dict[timeframe+'_10MA_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        # 5 MA
        x_dict[timeframe+'_5MA'] = deque([])
        # 5 MA log change from first candle close in view window
        x_dict[timeframe+'_5MA_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        # n most recent turning points ******************************************************************************************
        for i in range(number_of_most_recent_turning_points_per_each_view_window, 0, -1): # loop in reverse ... from n till 1
            # turning point's position from current candle
            if i == 11 or i == 12 or i == 13: suffix = 'th'
            elif str(i)[-1] == '1': suffix = 'st'
            elif str(i)[-1] == '2': suffix = 'nd'
            elif str(i)[-1] == '3': suffix = 'rd'
            else: suffix = 'th'
            position = str(i) + suffix
            # n most recent turning point
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Is_A_High'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Is_A_Low'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Index_In_View_Window'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Y_Distance_From_Previous_Turning_Point'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Y_Log_Distance_From_Previous_Turning_Point'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_X_Steps_From_Previous_Turning_Point'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_X_Log_Steps_From_Previous_Turning_Point'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Slope_From_Previous_Turning_Point'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Slope_Log_From_Previous_Turning_Point'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Broke_Structure_Up'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Broke_Structure_Down'] = deque([])
        # ***********************************************************************************************************************
    # *************************************************************************************************************************************

    # loop through each timeframe's df and populate df dict *******************************************************************************
    for timeframe in timeframes:
        # get the append frequency based on the timeframe to match smallest timeframe *******************************************
        if timeframe == 'Daily': append_frequency = 96; dates = daily_dates; opens = daily_opens; highs = daily_highs; lows = daily_lows; closes = daily_closes
        elif timeframe == 'H4': append_frequency = 16; dates = h4_dates; opens = h4_opens; highs = h4_highs; lows = h4_lows; closes = h4_closes
        elif timeframe == 'H1': append_frequency = 4; dates = h1_dates; opens = h1_opens; highs = h1_highs; lows = h1_lows; closes = h1_closes
        elif timeframe == 'M30': append_frequency = 2; dates = m30_dates; opens = m30_opens; highs = m30_highs; lows = m30_lows; closes = m30_closes
        elif timeframe == 'M15': append_frequency = 1; dates = m15_dates; opens = m15_opens; highs = m15_highs; lows = m15_lows; closes = m15_closes
        # ***********************************************************************************************************************

        # populate df dict ******************************************************************************************************
        for i in tqdm(range(view_window+3, len(closes)), desc="X Feature Engineering: "+timeframe, unit="row"): # we start from index = view_window+3 (there's a part in the loop where we need to consider the 2 last candlesticks as well)
            # get all turning points in view window *******************************************************************
            # initialize dict to store turning points *******************************************************
            turning_points_dict = {}
            turning_points_dict['Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_Close'] = deque([])
            turning_points_dict['Turning_Point_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
            turning_points_dict['Turning_Point_Close_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
            turning_points_dict['Turning_Point_Is_A_High'] = deque([])
            turning_points_dict['Turning_Point_Is_A_Low'] = deque([])
            turning_points_dict['Turning_Point_Index_In_View_Window'] = deque([])
            turning_points_dict['Turning_Point_Candlestick_Index'] = deque([])
            turning_points_dict['Turning_Point_Y_Distance_From_Previous_Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_Y_Log_Distance_From_Previous_Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_X_Steps_From_Previous_Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_X_Log_Steps_From_Previous_Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_Slope_From_Previous_Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_Slope_Log_From_Previous_Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_Broke_Structure_Up'] = deque([])
            turning_points_dict['Turning_Point_Broke_Structure_Down'] = deque([])
            # ***********************************************************************************************

            # first candle ohlc in view window
            first_candle_index_in_view_window = i - view_window
            first_candle_open_in_view_window = opens[first_candle_index_in_view_window]
            first_candle_high_in_view_window = highs[first_candle_index_in_view_window]
            first_candle_low_in_view_window = lows[first_candle_index_in_view_window]
            first_candle_close_in_view_window = closes[first_candle_index_in_view_window]

            # go through view window to find turning points *************************************************
            for j in range(view_window):
                # whether there's a new turning point or not
                new_turning_point = False

                # initialize variables
                turning_point = None; turning_point_close = None; turning_point_log_change_from_first_candle_close_in_view_window = None
                turning_point_close_log_change_from_first_candle_close_in_view_window = None
                turning_point_is_a_high = None; turning_point_is_a_low = None
                turning_point_index_in_view_window = None; turning_point_candlestick_index = None
                turning_point_y_distance_from_previous_turning_point = None; turning_point_y_log_distance_from_previous_turning_point = None
                turning_point_x_steps_from_previous_turning_point = None
                turning_point_slope_from_previous_turning_point = None; turning_point_slope_log_from_previous_turning_point = None
                turning_point_broke_structure_up = None; turning_point_broke_structure_down = None

                # current view window candlestick's index
                current_view_window_candlestick_index = i-j

                # get 3 recent candle highs
                most_recent_high = highs[current_view_window_candlestick_index]
                second_most_recent_high = highs[current_view_window_candlestick_index-1]
                third_most_recent_high = highs[current_view_window_candlestick_index-2]

                # get 3 recent candle lows
                most_recent_low = lows[current_view_window_candlestick_index]
                second_most_recent_low = lows[current_view_window_candlestick_index-1]
                third_most_recent_low = lows[current_view_window_candlestick_index-2]

                # get previous open and close
                previous_open = opens[current_view_window_candlestick_index-1]
                previous_close = closes[current_view_window_candlestick_index-1]

                # turning point's index in main dataset
                turning_point_candlestick_index = current_view_window_candlestick_index-1

                # steps from last turning point
                last_turning_point_index = turning_point_candlestick_index - first_candle_index_in_view_window if len(turning_points_dict['Turning_Point']) == 0 else turning_points_dict['Turning_Point_Candlestick_Index'][-1]
                current_turning_point_index = turning_point_candlestick_index
                steps_from_last_turning_point = current_turning_point_index - last_turning_point_index
                log_change_in_x = np.log(current_turning_point_index / last_turning_point_index)

                # check for new high
                if second_most_recent_high >= third_most_recent_high and second_most_recent_high >= most_recent_high:
                    # high's parameters
                    turning_point = second_most_recent_high # high's value
                    turning_point_close = previous_close if previous_close >= previous_open else previous_open # high's close/open depending on candlestick type
                    turning_point_log_change_from_first_candle_close_in_view_window = np.log(turning_point / first_candle_close_in_view_window) # high's log change from first candle close
                    turning_point_close_log_change_from_first_candle_close_in_view_window = np.log(turning_point_close / first_candle_close_in_view_window) # high close's log change from first candle close
                    turning_point_is_a_high = 1 # 0 if false, 1 if true
                    turning_point_is_a_low = 0 # 0 if false, 1 if true
                    turning_point_index_in_view_window = j-1 # high's index in view window
                    turning_point_y_distance_from_previous_turning_point = turning_point - first_candle_low_in_view_window if len(turning_points_dict['Turning_Point']) == 0 else turning_point - turning_points_dict['Turning_Point'][-1] # change in y
                    turning_point_y_log_distance_from_previous_turning_point = np.log(turning_point / first_candle_low_in_view_window) if len(turning_points_dict['Turning_Point']) == 0 else np.log(turning_point / turning_points_dict['Turning_Point'][-1]) # log change in y
                    turning_point_x_steps_from_previous_turning_point = steps_from_last_turning_point
                    turning_point_x_log_steps_from_previous_turning_point = log_change_in_x
                    turning_point_slope_from_previous_turning_point = turning_point_y_distance_from_previous_turning_point / turning_point_x_steps_from_previous_turning_point # slope / gradient
                    turning_point_slope_log_from_previous_turning_point =  turning_point_y_log_distance_from_previous_turning_point / log_change_in_x # log slope / gradient
                    turning_point_broke_structure_up = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0]) == 0 else 1 if turning_point > turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    turning_point_broke_structure_down = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0]) == 0 else 1 if turning_point < turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    # append parameter values to turning points dict
                    turning_points_dict['Turning_Point'].append(turning_point)
                    turning_points_dict['Turning_Point_Close'].append(turning_point_close)
                    turning_points_dict['Turning_Point_Log_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_log_change_from_first_candle_close_in_view_window)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_close_log_change_from_first_candle_close_in_view_window)
                    turning_points_dict['Turning_Point_Is_A_High'].append(turning_point_is_a_high)
                    turning_points_dict['Turning_Point_Is_A_Low'].append(turning_point_is_a_low)
                    turning_points_dict['Turning_Point_Index_In_View_Window'].append(turning_point_index_in_view_window)
                    turning_points_dict['Turning_Point_Candlestick_Index'].append(turning_point_candlestick_index)
                    turning_points_dict['Turning_Point_Y_Distance_From_Previous_Turning_Point'].append(turning_point_y_distance_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Y_Log_Distance_From_Previous_Turning_Point'].append(turning_point_y_log_distance_from_previous_turning_point)
                    turning_points_dict['Turning_Point_X_Steps_From_Previous_Turning_Point'].append(turning_point_x_steps_from_previous_turning_point)
                    turning_points_dict['Turning_Point_X_Log_Steps_From_Previous_Turning_Point'].append(turning_point_x_log_steps_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Slope_From_Previous_Turning_Point'].append(turning_point_slope_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Slope_Log_From_Previous_Turning_Point'].append(turning_point_slope_log_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Broke_Structure_Up'].append(turning_point_broke_structure_up)
                    turning_points_dict['Turning_Point_Broke_Structure_Down'].append(turning_point_broke_structure_down)

                # check for new low
                if second_most_recent_low <= third_most_recent_low and second_most_recent_low <= most_recent_low:
                    # low's parameters
                    turning_point = second_most_recent_low # low's value
                    turning_point_close = previous_open if previous_open <= previous_close else previous_close # low's close/open depending on candlestick type
                    turning_point_log_change_from_first_candle_close_in_view_window = np.log(turning_point / first_candle_close_in_view_window) # low's log change from first candle close
                    turning_point_close_log_change_from_first_candle_close_in_view_window = np.log(turning_point_close / first_candle_close_in_view_window) # low close's log change from first candle close
                    turning_point_is_a_high = 0 # 0 if false, 1 if true
                    turning_point_is_a_low = 1 # 0 if false, 1 if true
                    turning_point_index_in_view_window = j-1 # low's index in view window
                    turning_point_y_distance_from_previous_turning_point = turning_point - first_candle_high_in_view_window if len(turning_points_dict['Turning_Point']) == 0 else turning_point - turning_points_dict['Turning_Point'][-1] # change in y
                    turning_point_y_log_distance_from_previous_turning_point = np.log(turning_point / first_candle_high_in_view_window) if len(turning_points_dict['Turning_Point']) == 0 else np.log(turning_point / turning_points_dict['Turning_Point'][-1]) # log change in y
                    turning_point_x_steps_from_previous_turning_point = steps_from_last_turning_point
                    turning_point_x_log_steps_from_previous_turning_point = log_change_in_x
                    turning_point_slope_from_previous_turning_point = turning_point_y_distance_from_previous_turning_point / turning_point_x_steps_from_previous_turning_point # slope / gradient
                    turning_point_slope_log_from_previous_turning_point = turning_point_y_log_distance_from_previous_turning_point / log_change_in_x # log slope / gradient
                    turning_point_broke_structure_up = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0]) == 0 else 1 if turning_point > turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    turning_point_broke_structure_down = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0]) == 0 else 1 if turning_point < turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    # append parameter values to turning points dict
                    turning_points_dict['Turning_Point'].append(turning_point)
                    turning_points_dict['Turning_Point_Close'].append(turning_point_close)
                    turning_points_dict['Turning_Point_Log_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_log_change_from_first_candle_close_in_view_window)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_close_log_change_from_first_candle_close_in_view_window)
                    turning_points_dict['Turning_Point_Is_A_High'].append(turning_point_is_a_high)
                    turning_points_dict['Turning_Point_Is_A_Low'].append(turning_point_is_a_low)
                    turning_points_dict['Turning_Point_Index_In_View_Window'].append(turning_point_index_in_view_window)
                    turning_points_dict['Turning_Point_Candlestick_Index'].append(turning_point_candlestick_index)
                    turning_points_dict['Turning_Point_Y_Distance_From_Previous_Turning_Point'].append(turning_point_y_distance_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Y_Log_Distance_From_Previous_Turning_Point'].append(turning_point_y_log_distance_from_previous_turning_point)
                    turning_points_dict['Turning_Point_X_Steps_From_Previous_Turning_Point'].append(turning_point_x_steps_from_previous_turning_point)
                    turning_points_dict['Turning_Point_X_Log_Steps_From_Previous_Turning_Point'].append(turning_point_x_log_steps_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Slope_From_Previous_Turning_Point'].append(turning_point_slope_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Slope_Log_From_Previous_Turning_Point'].append(turning_point_slope_log_from_previous_turning_point)
                    turning_points_dict['Turning_Point_Broke_Structure_Up'].append(turning_point_broke_structure_up)
                    turning_points_dict['Turning_Point_Broke_Structure_Down'].append(turning_point_broke_structure_down)
            # ***********************************************************************************************
            # *********************************************************************************************************

            # array of all closes up until i, i included
            all_closes_till_i = closes[:i+1] # i+1 so that i is included

            # current ohlc data, plus date
            current_candle_date = dates[i]
            current_candle_open = opens[i]
            current_candle_high = highs[i]
            current_candle_low = lows[i]
            current_candle_close = closes[i]

            # populate df dict according to timeframe's append frequency **********************************************
            for k in range(append_frequency):
                # timestamp
                if timeframe == 'M15': x_dict[timeframe+'_Timestamp'].append(current_candle_date)
                # ohlc data
                x_dict[timeframe+'_Open'].append(current_candle_open)
                x_dict[timeframe+'_High'].append(current_candle_high)
                x_dict[timeframe+'_Low'].append(current_candle_low)
                x_dict[timeframe+'_Close'].append(current_candle_close)
                # ohlc data's log change from first candle in the view window
                x_dict[timeframe+'_Open_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(current_candle_open / first_candle_close_in_view_window))
                x_dict[timeframe+'_High_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(current_candle_high / first_candle_close_in_view_window))
                x_dict[timeframe+'_Low_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(current_candle_low / first_candle_close_in_view_window))
                x_dict[timeframe+'_Close_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(current_candle_close / first_candle_close_in_view_window))
                # candlestick types
                x_dict[timeframe+'_Bullish'].append(1 if current_candle_close > current_candle_close else 0)
                x_dict[timeframe+'_Bearish'].append(1 if current_candle_close < current_candle_open else 0)
                x_dict[timeframe+'_Doji'].append(1 if current_candle_close == current_candle_open else 0)
                # wicks
                x_dict[timeframe+'_Upper_Wick'].append(current_candle_high - current_candle_close if current_candle_close >= current_candle_open else current_candle_high - current_candle_open)
                x_dict[timeframe+'_Lower_Wick'].append(current_candle_close - current_candle_low if current_candle_close < current_candle_open else current_candle_open - current_candle_low)
                # wicks logs
                x_dict[timeframe+'_Upper_Wick_Log'].append(np.log(current_candle_high / current_candle_close) if current_candle_close >= current_candle_open else np.log(current_candle_high / current_candle_open))
                x_dict[timeframe+'_Lower_Wick_Log'].append(np.log(current_candle_close / current_candle_low) if current_candle_close < current_candle_open else np.log(current_candle_open / current_candle_low))
                # body size
                x_dict[timeframe+'_Body_Size'].append(current_candle_close - current_candle_open)
                # body size logs
                x_dict[timeframe+'_Body_Size_Log'].append(np.log(current_candle_close / current_candle_open))
                # candlestick size
                x_dict[timeframe+'_Candlestick_Size'].append(current_candle_high - current_candle_low)
                # candlestick size logs
                x_dict[timeframe+'_Candlestick_Size_Log'].append(np.log(current_candle_high / current_candle_low))
                # 50 MA
                ma50 = np.sum(all_closes_till_i[-50:]) / 50
                x_dict[timeframe+'_50MA'].append(ma50)
                # 50 MA log change from first candle close in view window
                x_dict[timeframe+'_50MA_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(ma50 / first_candle_close_in_view_window))
                # 25 MA 
                ma25 = np.sum(all_closes_till_i[-25:]) / 25
                x_dict[timeframe+'_25MA'].append(ma25)
                # 25 MA log change from first candle close in view window
                x_dict[timeframe+'_25MA_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(ma25 / first_candle_close_in_view_window))
                # 10 MA
                ma10 = np.sum(all_closes_till_i[-10:]) / 10
                x_dict[timeframe+'_10MA'].append(ma10)
                # 10 MA log change from first candle close in view window
                x_dict[timeframe+'_10MA_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(ma10 / first_candle_close_in_view_window))
                # 5 MA
                ma5 = np.sum(all_closes_till_i[-5:]) / 5
                x_dict[timeframe+'_5MA'].append(ma5)
                # 5 MA log change from first candle close in view window
                x_dict[timeframe+'_5MA_Log_Change_From_First_Candle_Close_In_View_Window'].append(np.log(ma5 / first_candle_close_in_view_window))
                # n most recent turning points **************************************************************
                for j in range(number_of_most_recent_turning_points_per_each_view_window, 0, -1): # loop in reverse ... from n till 1
                    # turning point's position from current candle
                    if j == 11 or j == 12 or j == 13: suffix = 'th'
                    elif str(j)[-1] == '1': suffix = 'st'
                    elif str(j)[-1] == '2': suffix = 'nd'
                    elif str(j)[-1] == '3': suffix = 'rd'
                    else: suffix = 'th'
                    position = str(j) + suffix
                    # n most recent turning point
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point'].append(turning_points_dict['Turning_Point'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close'].append(turning_points_dict['Turning_Point_Close'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_First_Candle_Close_In_View_Window'].append(turning_points_dict['Turning_Point_Log_Change_From_First_Candle_Close_In_View_Window'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_First_Candle_Close_In_View_Window'].append(turning_points_dict['Turning_Point_Close_Log_Change_From_First_Candle_Close_In_View_Window'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Is_A_High'].append(turning_points_dict['Turning_Point_Is_A_High'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Is_A_Low'].append(turning_points_dict['Turning_Point_Is_A_Low'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Index_In_View_Window'].append(turning_points_dict['Turning_Point_Index_In_View_Window'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Y_Distance_From_Previous_Turning_Point'].append(turning_points_dict['Turning_Point_Y_Distance_From_Previous_Turning_Point'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Y_Log_Distance_From_Previous_Turning_Point'].append(turning_points_dict['Turning_Point_Y_Log_Distance_From_Previous_Turning_Point'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_X_Steps_From_Previous_Turning_Point'].append(turning_points_dict['Turning_Point_X_Steps_From_Previous_Turning_Point'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_X_Log_Steps_From_Previous_Turning_Point'].append(turning_points_dict['Turning_Point_X_Log_Steps_From_Previous_Turning_Point'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Slope_From_Previous_Turning_Point'].append(turning_points_dict['Turning_Point_Slope_From_Previous_Turning_Point'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Slope_Log_From_Previous_Turning_Point'].append(turning_points_dict['Turning_Point_Slope_Log_From_Previous_Turning_Point'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Broke_Structure_Up'].append(turning_points_dict['Turning_Point_Broke_Structure_Up'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Broke_Structure_Down'].append(turning_points_dict['Turning_Point_Broke_Structure_Down'][-j])
                # *******************************************************************************************
            # *********************************************************************************************************
        # ***********************************************************************************************************************
    # *************************************************************************************************************************************

    # cut all x_dict arrays to last n elements to match m15 data **************************************************************************
    m15_length = len(x_dict['M15_Timestamp'])
    x_column_list = list(x_dict.keys())
    for key in x_column_list:
        x_dict[key] = np.array(x_dict[key])[-m15_length:]
    # *************************************************************************************************************************************

    # build pandas dataframe using x_dict *************************************************************************************************
    x_features_dataframe = pd.DataFrame(x_dict)
    print('\n\nX Features Dataset:\n', x_features_dataframe.head(), '\n\n')
    # *************************************************************************************************************************************

    # return x_features_dataframe, and x_column_list
    return x_features_dataframe, x_column_list