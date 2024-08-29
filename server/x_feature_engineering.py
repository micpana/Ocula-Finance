import pandas as pd
import numpy as np
from collections import deque
from tqdm import tqdm

# feature engineering
def engineer_x(ohlc_data_dict, timeframes, entry_timeframe):
    # View Window / Number of candlesticks to look at / Number of candlesticks in viewport
    view_window = 100

    # number of most recent turning points per each view window
    number_of_most_recent_turning_points_per_each_view_window = 3

    # ma types
    ma_types = np.array(['Simple', 'Exponential', 'Smoothed', 'Weighted'])

    # larger ma type
    larger_ma_type = 'Default' # type in ma type / Default ... Default will make larger_ma_type the same as ma_type in the loop
    
    # ma periods
    sma_periods = np.array([])
    ema_periods = np.array([50, 25, 10, 5])
    smoothed_periods = np.array([])
    weighted_periods = np.array([])

    # rsi periods
    rsi_periods = np.array([14])
    
    # std periods
    std_periods = np.array([20])

    # ma deep features
    ma_deep_features = True

    # ichimoku on
    ichimoku_on = True

    # ichimoku deep feature comparison
    ichimoku_deep_feature_comparison = True

    # ichimoku own feature comparison 
    ichimoku_own_feature_comparison = True

    # candlestick patterns on
    candlestick_patterns_on = False

    # initialize x dict *******************************************************************************************************************
    x_dict = {}
    for timeframe in timeframes:
        # timestamp
        x_dict[timeframe+'_Timestamp'] = deque([])
        # ohlc data
        x_dict[timeframe+'_Open'] = deque([])
        x_dict[timeframe+'_High'] = deque([])
        x_dict[timeframe+'_Low'] = deque([])
        x_dict[timeframe+'_Close'] = deque([])
        # ohlc change from first candle in view window
        x_dict[timeframe+'_Open_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        x_dict[timeframe+'_High_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        x_dict[timeframe+'_Low_Change_From_First_Candle_Close_In_View_Window'] = deque([])
        x_dict[timeframe+'_Close_Change_From_First_Candle_Close_In_View_Window'] = deque([])
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
        # candlestick patterns **************************************************************************************************
        if candlestick_patterns_on == True:
            x_dict[timeframe+'_Bearish_Harami'] = deque([])
            x_dict[timeframe+'_Bearish_Harami_Cross'] = deque([])
            x_dict[timeframe+'_Bearish_3_Method_Formation'] = deque([])
            x_dict[timeframe+'_Bullish_3_Method_Formation'] = deque([])
            x_dict[timeframe+'_Bullish_Harami'] = deque([])
            x_dict[timeframe+'_Bullish_Harami_Cross'] = deque([])
            x_dict[timeframe+'_Dark_Cloud_Cover'] = deque([])
            x_dict[timeframe+'_Engulfing_Bearish_Line'] = deque([])
            x_dict[timeframe+'_Engulfing_Bullish_Line'] = deque([])
            x_dict[timeframe+'_Evening_Doji_Star'] = deque([])
            x_dict[timeframe+'_Evening_Star'] = deque([])
            x_dict[timeframe+'_Falling_Window'] = deque([])
            x_dict[timeframe+'_Morning_Doji_Star'] = deque([])
            x_dict[timeframe+'_Morning_Star'] = deque([])
            x_dict[timeframe+'_On_Neckline'] = deque([])
            x_dict[timeframe+'_Three_Black_Crows'] = deque([])
            x_dict[timeframe+'_Three_White_Soldiers'] = deque([])
            x_dict[timeframe+'_Tweezer_Bottoms'] = deque([])
            x_dict[timeframe+'_Tweezer_Tops'] = deque([])
            x_dict[timeframe+'_Doji_Star'] = deque([])
            x_dict[timeframe+'_Piercing_Line'] = deque([])
            x_dict[timeframe+'_Rising_Window'] = deque([])
            # x_dict[timeframe+'_Doji'] = deque([])  # already done for candlestick type above  (bullish / bearish / doji)
            x_dict[timeframe+'_Dragon_Fly_Doji'] = deque([])
            x_dict[timeframe+'_Gravestone_Doji'] = deque([])
            x_dict[timeframe+'_Hanging_Man'] = deque([])
            x_dict[timeframe+'_Hammer'] = deque([])
            x_dict[timeframe+'_Inverted_Black_Hammer'] = deque([])
            x_dict[timeframe+'_Inverted_Hammer'] = deque([])
            x_dict[timeframe+'_Long_Lower_Shadow'] = deque([])
            x_dict[timeframe+'_Long_Upper_Shadow'] = deque([])
            x_dict[timeframe+'_Marubozu'] = deque([])
            x_dict[timeframe+'_Shooting_Star'] = deque([])
            x_dict[timeframe+'_Shaven_Bottom'] = deque([])
            x_dict[timeframe+'_Shaven_Head'] = deque([])
        # ***********************************************************************************************************************
        # MAs *******************************************************************************************************************
        for ma_type in ma_types:
            # periods
            if ma_type == 'Simple': periods = sma_periods
            elif ma_type == 'Exponential': periods = ema_periods
            elif ma_type == 'Smoothed': periods = smoothed_periods
            elif ma_type == 'Weighted': periods = weighted_periods

            # loop through ma periods
            for z in range(len(periods)):
                # MA period
                period = periods[z]
                # MA
                x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA'] = deque([])
                # ma deep features
                if ma_deep_features == True:
                    # MA change from first candle close in view window
                    x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                    # MA log change from first candle close in view window
                    x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                    # current close - MA
                    x_dict[timeframe+'_Close-'+str(period)+'_'+ma_type+'_MA'] = deque([])
                    # MA log change from current close
                    x_dict[timeframe+'_Close_'+str(period)+'_'+ma_type+'_MA_Log_Change'] = deque([])
                    # current open - MA
                    x_dict[timeframe+'_Open-'+str(period)+'_'+ma_type+'_MA'] = deque([])
                    # MA log change from current open
                    x_dict[timeframe+'_Open_'+str(period)+'_'+ma_type+'_MA_Log_Change'] = deque([])
                    # current high - MA
                    x_dict[timeframe+'_High-'+str(period)+'_'+ma_type+'_MA'] = deque([])
                    # MA log change from current high
                    x_dict[timeframe+'_High_'+str(period)+'_'+ma_type+'_MA_Log_Change'] = deque([])
                    # current low - MA
                    x_dict[timeframe+'_Low-'+str(period)+'_'+ma_type+'_MA'] = deque([])
                    # MA log change from current low
                    x_dict[timeframe+'_Low_'+str(period)+'_'+ma_type+'_MA_Log_Change'] = deque([])
                    # difference between current MA and every other MA before it **************************
                    if z != 0:
                        for y in range(len(periods[:z])):
                            # larger MA period
                            larger_period = periods[y]
                            # current MA - larger MA
                            x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA-'+str(larger_period)+'_'+ma_type+'_MA'] = deque([])
                            # current MA larger MA Log change
                            x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA_'+str(larger_period)+'_'+ma_type+'_MA_Log_Change'] = deque([])
                    # ***************************************************************************************
        # ***********************************************************************************************************************
        # RSIs ******************************************************************************************************************
        for period in rsi_periods:
            # period rsi
            x_dict[timeframe+'_'+str(period)+'_Period_RSI'] = deque([])
        # ***********************************************************************************************************************
        # standard deviations ***************************************************************************************************
        for period in std_periods:
            # period standard deviation
            x_dict[timeframe+'_'+str(period)+'_Period_Std'] = deque([])
        # ***********************************************************************************************************************
        # ichimoku kinko hyo ****************************************************************************************************
        if ichimoku_on == True:
            # tenkan-sen **********************************************************************************************
            # tenkan-sen values
            x_dict[timeframe+'_Tenkan-sen'] = deque([])
            # ichimoku deep features ************************************************************************
            if ichimoku_deep_feature_comparison == True:
                # change from first candle close in view window
                x_dict[timeframe+'_Tenkan-sen_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # log change from first candle close in view window
                x_dict[timeframe+'_Tenkan-sen_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # current close - tenkan-sen
                x_dict[timeframe+'_Current_Close-Tenkan-sen'] = deque([])
                # tenkan-sen log change from current close
                x_dict[timeframe+'_Close_Tenkan-sen_Log_Change'] = deque([])
                # current open - tenkan-sen
                x_dict[timeframe+'_Open-Tenkan-sen'] = deque([])
                # tenkan-sen log change from current open
                x_dict[timeframe+'_Open_Tenkan-sen_Log_Change'] = deque([])
                # current high - tenkan-sen
                x_dict[timeframe+'_High-Tenkan-sen'] = deque([])
                # tenkan-sen log change from current high
                x_dict[timeframe+'_High_Tenkan-sen_Log_Change'] = deque([])
                # current low - tenkan-sen
                x_dict[timeframe+'_Low-Tenkan-sen'] = deque([])
                # tenkan-sen log change from current low
                x_dict[timeframe+'_Low_Tenkan-sen_Log_Change'] = deque([])
                # ichimoku own feature comparison *************************************************
                if ichimoku_own_feature_comparison == True:
                    # tenkan-sen - kijun-sen
                    x_dict[timeframe+'_Tenkan-sen-Kijun-sen'] = deque([])
                    # tenkan-sen log change from kijun-sen
                    x_dict[timeframe+'_Tenkan-sen_Kijun-sen_Log_Change'] = deque([])
                # *********************************************************************************
            # ***********************************************************************************************
            # *********************************************************************************************************
            # kijun-sen ***********************************************************************************************
            # kijun-sen values
            x_dict[timeframe+'_Kijun-sen'] = deque([])
            # ichimoku deep features ************************************************************************
            if ichimoku_deep_feature_comparison == True:
                # change from first candle close in view window
                x_dict[timeframe+'_Kijun-sen_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # log change from first candle close in view window
                x_dict[timeframe+'_Kijun-sen_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # current close - kijun-sen
                x_dict[timeframe+'_Current_Close-Kijun-sen'] = deque([])
                # kijun-sen log change from current close
                x_dict[timeframe+'_Close_Kijun-sen_Log_Change'] = deque([])
                # current open - kijun-sen
                x_dict[timeframe+'_Open-Kijun-sen'] = deque([])
                # kijun-sen log change from current open
                x_dict[timeframe+'_Open_Kijun-sen_Log_Change'] = deque([])
                # current high - kijun-sen
                x_dict[timeframe+'_High-Kijun-sen'] = deque([])
                # kijun-sen log change from current high
                x_dict[timeframe+'_High_Kijun-sen_Log_Change'] = deque([])
                # current low - kijun-sen
                x_dict[timeframe+'_Low-Kijun-sen'] = deque([])
                # kijun-sen log change from current low
                x_dict[timeframe+'_Low_Kijun-sen_Log_Change'] = deque([])
            # ***********************************************************************************************
            # *********************************************************************************************************
            # chikou span *********************************************************************************************
            # chikou span values
            x_dict[timeframe+'_Chikou_Span'] = deque([])
            # senkou span a (from 26 periods back) - chikou span
            x_dict[timeframe+'_Senkou_Span_A-Chikou_Span'] = deque([])
            # chikou span log change from senkou span a (from 26 periods back)
            x_dict[timeframe+'_Senkou_Span_A_Chikou_Span_Log_Change'] = deque([])
            # senkou span b (from 26 periods back) - chikou span
            x_dict[timeframe+'_Senkou_Span_B-Chikou_Span'] = deque([])
            # chikou span log change from senkou span b (from 26 periods back)
            x_dict[timeframe+'_Senkou_Span_B_Chikou_Span_Log_Change'] = deque([])
            # *********************************************************************************************************
            # senkou span a *******************************************************************************************
            # senkou span a values
            x_dict[timeframe+'_Senkou_Span_A'] = deque([])
            # ichimoku deep features ************************************************************************
            if ichimoku_deep_feature_comparison == True:
                # change from first candle close in view window
                x_dict[timeframe+'_Senkou_Span_A_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # log change from first candle close in view window
                x_dict[timeframe+'_Senkou_Span_A_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # current close - senkou span a
                x_dict[timeframe+'_Current_Close-Senkou_Span_A'] = deque([])
                # senkou span a log change from current close
                x_dict[timeframe+'_Close_Senkou_Span_A_Log_Change'] = deque([])
                # current open - senkou span a
                x_dict[timeframe+'_Open-Senkou_Span_A'] = deque([])
                # senkou span a log change from current open
                x_dict[timeframe+'_Open_Senkou_Span_A_Log_Change'] = deque([])
                # current high - senkou span a
                x_dict[timeframe+'_High-Senkou_Span_A'] = deque([])
                # senkou span a log change from current high
                x_dict[timeframe+'_High_Senkou_Span_A_Log_Change'] = deque([])
                # current low - senkou span a
                x_dict[timeframe+'_Low-Senkou_Span_A'] = deque([])
                # senkou span a log change from current low
                x_dict[timeframe+'_Low_Senkou_Span_A_Log_Change'] = deque([])
                # ichimoku own feature comparison *************************************************
                if ichimoku_own_feature_comparison == True:
                    # senkou span a - senkou span b
                    x_dict[timeframe+'_Senkou_Span_A-Senkou_Span_B'] = deque([])
                    # senkou span a log change from senkou span b
                    x_dict[timeframe+'_Senkou_Span_A_Senkou_Span_B_Log_Change'] = deque([])
                # *********************************************************************************
            # ***********************************************************************************************
            # *************************************************************************************************************
            # senkou span b ***********************************************************************************************
            # senkou span b values
            x_dict[timeframe+'_Senkou_Span_B'] = deque([])
            # ichimoku deep features ****************************************************************************
            if ichimoku_deep_feature_comparison == True:
                # change from first candle close in view window
                x_dict[timeframe+'_Senkou_Span_B_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # log change from first candle close in view window
                x_dict[timeframe+'_Senkou_Span_B_Log_Change_From_First_Candle_Close_In_View_Window'] = deque([])
                # current close - senkou span b
                x_dict[timeframe+'_Current_Close-Senkou_Span_B'] = deque([])
                # senkou span b log change from current close
                x_dict[timeframe+'_Close_Senkou_Span_B_Log_Change'] = deque([])
                # current open - senkou span b
                x_dict[timeframe+'_Open-Senkou_Span_B'] = deque([])
                # senkou span b log change from current open
                x_dict[timeframe+'_Open_Senkou_Span_B_Log_Change'] = deque([])
                # current high - senkou span b
                x_dict[timeframe+'_High-Senkou_Span_B'] = deque([])
                # senkou span b log change from current high
                x_dict[timeframe+'_High_Senkou_Span_B_Log_Change'] = deque([])
                # current low - senkou span b
                x_dict[timeframe+'_Low-Senkou_Span_B'] = deque([])
                # senkou span b log change from current low
                x_dict[timeframe+'_Low_Senkou_Span_B_Log_Change'] = deque([])
            # ***************************************************************************************************
            # *************************************************************************************************************
        # ***********************************************************************************************************************
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
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Change_From_First_Candle_Close_In_View_Window'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Change_From_First_Candle_Close_In_View_Window'] = deque([])
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
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_Close'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_Close'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_Close'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_Close'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_Open'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_Open'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_Open'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_Open'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_High'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_High'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_High'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_High'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_Low'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_Low'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_Low'] = deque([])
            x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_Low'] = deque([])
        # ***********************************************************************************************************************
    # *************************************************************************************************************************************

    # function for calculating RSI ********************************************************************************************************
    def calculate_rsi(prices, period=14):
        # calculate daily price changes
        deltas = np.diff(prices)
        
        # separate positive and negative price changes
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        # calculate the average gains and losses over the specified period
        avg_gain = np.zeros_like(prices)
        avg_loss = np.zeros_like(prices)
        
        avg_gain[period] = np.mean(gains[:period])
        avg_loss[period] = np.mean(losses[:period])
        
        # calculate the average gains and losses for the rest of the array
        for i in range(period + 1, len(prices)):
            avg_gain[i] = (avg_gain[i - 1] * (period - 1) + gains[i - 1]) / period
            avg_loss[i] = (avg_loss[i - 1] * (period - 1) + losses[i - 1]) / period
        
        # calculate Relative Strength (RS)
        rs = avg_gain / avg_loss
        
        # calculate RSI
        rsi = 100 - (100 / (1 + rs))
        
        # return most recent rsi value
        return rsi[-1]
    # *************************************************************************************************************************************

    # function for calculating typical price **********************************************************************************************
    def calculate_typical_price(close, open, high, low):
        return (close + open + high + low) / 4
    # *************************************************************************************************************************************

    # function for calculating standard deviation ****************************************************************************************
    def calculate_rolling_std(typical_prices, period=20):
        rolling_std = np.zeros_like(typical_prices)
        for i in range(period - 1, len(typical_prices)):
            rolling_std[i] = np.std(typical_prices[i - period + 1:i + 1])

        # return most recent std
        return rolling_std[-1]
    # *************************************************************************************************************************************

    # function for calculating simple moving average **************************************************************************************
    def calculate_simple_ma(values, period):
        if len(values) < period:
            raise ValueError("(Simple MA) The length of the values array must be greater than the period.")

        sma = np.zeros_like(values, dtype=float)
        # ensure that we only calculate SMA for periods where there is enough data
        for i in range(period - 1, len(values)):
            sma[i] = np.mean(values[i - period + 1:i + 1])

        # return most recent sma
        return sma[-1]
    # *************************************************************************************************************************************

    # function for calculating exponential moving average *********************************************************************************
    def calculate_exponential_ma(values, period):
        if len(values) < period:
            raise ValueError("(Exponential MA) The length of the values array must be greater than the period.")

        ema_values = np.zeros_like(values)
        multiplier = 2 / (period + 1)
        ema_values[0] = values[0]
        for i in range(1, len(values)):
            ema_values[i] = (values[i] - ema_values[i-1]) * multiplier + ema_values[i-1]

        # return most recent ema
        return ema_values[-1]
    # *************************************************************************************************************************************

    # function for calculating smoothed moving average ************************************************************************************
    def calculate_smoothed_ma(values, period):
        if len(values) < period:
            raise ValueError("(Smoothed MA) The length of the values array must be greater than the period.")
        
        # initialize the SMA array
        sma = np.zeros_like(values, dtype=float)
        
        # calculate the first SMA value (sum of the first 'period' values divided by 'period')
        sma[period-1] = np.sum(values[:period]) / period
        
        # calculate the subsequent SMA values
        for i in range(period, len(values)):
            sma[i] = (sma[i-1] * (period - 1) + values[i]) / period
        
        # return most recent sma
        return sma[-1]
    # *************************************************************************************************************************************

    # function for calculating weighted moving average ************************************************************************************
    def calculate_weighted_ma(values, period):
        if len(values) < period:
            raise ValueError("(Weighted MA) The length of the values array must be greater than the period.")
    
        # initialize the WMA array
        wma = np.zeros_like(values, dtype=float)
        
        # calculate weights
        weights = np.arange(1, period + 1)
        
        # calculate WMA values
        for i in range(period - 1, len(values)):
            wma[i] = np.dot(values[i - period + 1:i + 1], weights) / weights.sum()
        
        # return most recent wma
        return wma[-1]
    # *************************************************************************************************************************************

    # function for calculating the the Ichimoku Kinko Hyo *********************************************************************************
    def calculate_ichimoku_kinko_hyo(highs, lows, closes):
        # periods
        tenkan_sen_period = 9
        kijun_sen_period = 26
        senkou_span_b_period = 52

        len_highs = len(highs)
        if len_highs < senkou_span_b_period or len_highs < kijun_sen_period or len_highs < tenkan_sen_period:
            raise ValueError("(Ichimoku) The length of the values array must be greater than the period.")

        # tenkan-sen value aka conversion line
        tenkan_sen = (np.amax(highs[-tenkan_sen_period:] + np.amin(lows[-tenkan_sen_period:]))) / 2

        # kijun-sen value aka base line
        kijun_sen = (np.amax(highs[-kijun_sen_period:] + np.amin(lows[-kijun_sen_period:]))) / 2

        # chikou span value aka lagging span (plotted 26 periods back)
        chikou_span = closes[-1]

        # senkou span A aka leading span A (faster cloud boundary plotted 26 periods into the future)
        senkou_span_a = (tenkan_sen + kijun_sen) / 2

        # senkou span B aka leading span B (slower cloud boundary plotted 26 periods into the future)
        senkou_span_b = (np.amax(highs[-senkou_span_b_period:] + np.amin(lows[-senkou_span_b_period:]))) / 2

        # return ichimoku values
        return tenkan_sen, kijun_sen, chikou_span, senkou_span_a, senkou_span_b
    # *************************************************************************************************************************************

    # loop through each timeframe's df and populate df dict *******************************************************************************
    for timeframe in timeframes:
        # get numpy arrays for dates, opens, highs, lows, and closes ************************************************************
        dates = ohlc_data_dict[timeframe]['time'].values
        opens = ohlc_data_dict[timeframe]['open'].values
        highs = ohlc_data_dict[timeframe]['high'].values
        lows = ohlc_data_dict[timeframe]['low'].values
        closes = ohlc_data_dict[timeframe]['close'].values
        # ***********************************************************************************************************************

        # get the append frequency based on the timeframe to match smallest timeframe *******************************************
        if timeframe == 'Daily': append_frequency = 96
        elif timeframe == 'H4': append_frequency = 16
        elif timeframe == 'H1': append_frequency = 4
        elif timeframe == 'M30': append_frequency = 2
        elif timeframe == 'M15': append_frequency = 1
        # ***********************************************************************************************************************

        # populate df dict ******************************************************************************************************
        for i in tqdm(range(view_window+3, len(closes)), desc="X Feature Engineering: "+timeframe, unit="row"): # we start from index = view_window+3 (there's a part in the loop where we need to consider the 2 last candlesticks as well)
            # get all turning points in view window *******************************************************************
            # initialize dict to store turning points *******************************************************
            turning_points_dict = {}
            turning_points_dict['Turning_Point'] = deque([])
            turning_points_dict['Turning_Point_Close'] = deque([])
            turning_points_dict['Turning_Point_Change_From_First_Candle_Close_In_View_Window'] = deque([])
            turning_points_dict['Turning_Point_Close_Change_From_First_Candle_Close_In_View_Window'] = deque([])
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
            turning_points_dict['Turning_Point_Subtracted_From_Current_Close'] = deque([])
            turning_points_dict['Turning_Point_Log_Change_From_Current_Close'] = deque([])
            turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Close'] = deque([])
            turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Close'] = deque([])
            turning_points_dict['Turning_Point_Subtracted_From_Current_Open'] = deque([])
            turning_points_dict['Turning_Point_Log_Change_From_Current_Open'] = deque([])
            turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Open'] = deque([])
            turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Open'] = deque([])
            turning_points_dict['Turning_Point_Subtracted_From_Current_High'] = deque([])
            turning_points_dict['Turning_Point_Log_Change_From_Current_High'] = deque([])
            turning_points_dict['Turning_Point_Close_Subtracted_From_Current_High'] = deque([])
            turning_points_dict['Turning_Point_Close_Log_Change_From_Current_High'] = deque([])
            turning_points_dict['Turning_Point_Subtracted_From_Current_Low'] = deque([])
            turning_points_dict['Turning_Point_Log_Change_From_Current_Low'] = deque([])
            turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Low'] = deque([])
            turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Low'] = deque([])
            # ***********************************************************************************************

            # first candle ohlc in view window
            first_candle_index_in_view_window = i - view_window
            first_candle_open_in_view_window = opens[first_candle_index_in_view_window]
            first_candle_high_in_view_window = highs[first_candle_index_in_view_window]
            first_candle_low_in_view_window = lows[first_candle_index_in_view_window]
            first_candle_close_in_view_window = closes[first_candle_index_in_view_window]

            # array of all closes up until i, i included
            all_closes_till_i = closes[:i+1] # i+1 so that i is included

            # current ohlc data, plus date
            candle_date_1 = dates[i]
            candle_open_1 = opens[i]
            candle_high_1 = highs[i]
            candle_low_1 = lows[i]
            candle_close_1 = closes[i]

            # ohlc data, 1 candle back
            candle_open_2 = opens[i-1]
            candle_high_2 = highs[i-1]
            candle_low_2 = lows[i-1]
            candle_close_2 = closes[i-1]

            # ohlc data, 2 candles back
            candle_open_3 = opens[i-2]
            candle_high_3 = highs[i-2]
            candle_low_3 = lows[i-2]
            candle_close_3 = closes[i-2]

            # ohlc data, 3 candles back
            candle_open_4 = opens[i-3]
            candle_high_4 = highs[i-3]
            candle_low_4 = lows[i-3]
            candle_close_4 = closes[i-3]

            # ohlc data, 4 candles back
            candle_open_5 = opens[i-4]
            candle_high_5 = highs[i-4]
            candle_low_5 = lows[i-4]
            candle_close_5 = closes[i-4]

            # go through view window to find turning points *************************************************
            for j in range(view_window):
                # whether there's a new turning point or not
                new_turning_point = False

                # initialize variables
                turning_point = None; turning_point_close = None; 
                turning_point_change_from_first_candle_close_in_view_window = None; turning_point_close_change_from_first_candle_close_in_view_window = None
                turning_point_log_change_from_first_candle_close_in_view_window = None; turning_point_close_log_change_from_first_candle_close_in_view_window = None
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
                    # high compared to first candle close in view window
                    turning_point_change_from_first_candle_close_in_view_window = turning_point - first_candle_close_in_view_window # high's change from first candle close
                    turning_point_close_change_from_first_candle_close_in_view_window = turning_point_close - first_candle_close_in_view_window # high close's change from first candle close
                    # high compared to first candle close in view window (log)
                    turning_point_log_change_from_first_candle_close_in_view_window = np.log(turning_point / first_candle_close_in_view_window) # high's log change from first candle close
                    turning_point_close_log_change_from_first_candle_close_in_view_window = np.log(turning_point_close / first_candle_close_in_view_window) # high close's log change from first candle close
                    # mark as high
                    turning_point_is_a_high = 1 # 0 if false, 1 if true
                    turning_point_is_a_low = 0 # 0 if false, 1 if true
                    # x and y positioning
                    turning_point_index_in_view_window = j-1 # high's index in view window
                    turning_point_y_distance_from_previous_turning_point = turning_point - first_candle_low_in_view_window if len(turning_points_dict['Turning_Point']) == 0 else turning_point - turning_points_dict['Turning_Point'][-1] # change in y
                    turning_point_y_log_distance_from_previous_turning_point = np.log(turning_point / first_candle_low_in_view_window) if len(turning_points_dict['Turning_Point']) == 0 else np.log(turning_point / turning_points_dict['Turning_Point'][-1]) # log change in y
                    turning_point_x_steps_from_previous_turning_point = steps_from_last_turning_point
                    turning_point_x_log_steps_from_previous_turning_point = log_change_in_x
                    # gradient
                    turning_point_slope_from_previous_turning_point = turning_point_y_distance_from_previous_turning_point / turning_point_x_steps_from_previous_turning_point # slope / gradient
                    turning_point_slope_log_from_previous_turning_point =  turning_point_y_log_distance_from_previous_turning_point / log_change_in_x # log slope / gradient
                    # market structure
                    turning_point_broke_structure_up = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0]) == 0 else 1 if turning_point > turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    turning_point_broke_structure_down = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0]) == 0 else 1 if turning_point < turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    # turning point high compared to current candle's close
                    current_close_minus_turning_point = candle_close_1 - turning_point
                    current_close_turning_point_log_change = np.log(candle_close_1 / turning_point)
                    current_close_minus_turning_point_close = candle_close_1 - turning_point_close
                    current_close_turning_point_close_log_change = np.log(candle_close_1 / turning_point_close)
                    # turning point high compared to current candle's open
                    current_open_minus_turning_point = candle_open_1 - turning_point
                    current_open_turning_point_log_change = np.log(candle_open_1 / turning_point)
                    current_open_minus_turning_point_close = candle_open_1 - turning_point_close
                    current_open_turning_point_close_log_change = np.log(candle_open_1 / turning_point_close)
                    # turning point high compared to current candle's high
                    current_high_minus_turning_point = candle_high_1 - turning_point
                    current_high_turning_point_log_change = np.log(candle_high_1 / turning_point)
                    current_high_minus_turning_point_close = candle_high_1 - turning_point_close
                    current_high_turning_point_close_log_change = np.log(candle_high_1 / turning_point_close)
                    # turning point high compared to current candle's low
                    current_low_minus_turning_point = candle_low_1 - turning_point
                    current_low_turning_point_log_change = np.log(candle_low_1 / turning_point)
                    current_low_minus_turning_point_close = candle_low_1 - turning_point_close
                    current_low_turning_point_close_log_change = np.log(candle_low_1 / turning_point_close)
                    # append parameter values to turning points dict
                    turning_points_dict['Turning_Point'].append(turning_point)
                    turning_points_dict['Turning_Point_Close'].append(turning_point_close)
                    turning_points_dict['Turning_Point_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_change_from_first_candle_close_in_view_window)
                    turning_points_dict['Turning_Point_Close_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_close_change_from_first_candle_close_in_view_window)
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
                    turning_points_dict['Turning_Point_Subtracted_From_Current_Close'].append(current_close_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_Close'].append(current_close_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Close'].append(current_close_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Close'].append(current_close_turning_point_close_log_change)
                    turning_points_dict['Turning_Point_Subtracted_From_Current_Open'].append(current_open_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_Open'].append(current_open_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Open'].append(current_open_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Open'].append(current_open_turning_point_close_log_change)
                    turning_points_dict['Turning_Point_Subtracted_From_Current_High'].append(current_high_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_High'].append(current_high_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_High'].append(current_high_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_High'].append(current_high_turning_point_close_log_change)
                    turning_points_dict['Turning_Point_Subtracted_From_Current_Low'].append(current_low_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_Low'].append(current_low_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Low'].append(current_low_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Low'].append(current_low_turning_point_close_log_change)

                # check for new low
                if second_most_recent_low <= third_most_recent_low and second_most_recent_low <= most_recent_low:
                    # low's parameters
                    turning_point = second_most_recent_low # low's value
                    turning_point_close = previous_open if previous_open <= previous_close else previous_close # low's close/open depending on candlestick type
                    # low compared to first candle in view window
                    turning_point_change_from_first_candle_close_in_view_window = turning_point - first_candle_close_in_view_window # low's change from first candle close
                    turning_point_close_change_from_first_candle_close_in_view_window = turning_point_close - first_candle_close_in_view_window # low close's change from first candle close
                    # low compared to first candle in view window (log)
                    turning_point_log_change_from_first_candle_close_in_view_window = np.log(turning_point / first_candle_close_in_view_window) # low's log change from first candle close
                    turning_point_close_log_change_from_first_candle_close_in_view_window = np.log(turning_point_close / first_candle_close_in_view_window) # low close's log change from first candle close
                    # mark as low
                    turning_point_is_a_high = 0 # 0 if false, 1 if true
                    turning_point_is_a_low = 1 # 0 if false, 1 if true
                    # x and y positioning
                    turning_point_index_in_view_window = j-1 # low's index in view window
                    turning_point_y_distance_from_previous_turning_point = turning_point - first_candle_high_in_view_window if len(turning_points_dict['Turning_Point']) == 0 else turning_point - turning_points_dict['Turning_Point'][-1] # change in y
                    turning_point_y_log_distance_from_previous_turning_point = np.log(turning_point / first_candle_high_in_view_window) if len(turning_points_dict['Turning_Point']) == 0 else np.log(turning_point / turning_points_dict['Turning_Point'][-1]) # log change in y
                    turning_point_x_steps_from_previous_turning_point = steps_from_last_turning_point
                    turning_point_x_log_steps_from_previous_turning_point = log_change_in_x
                    # gradient
                    turning_point_slope_from_previous_turning_point = turning_point_y_distance_from_previous_turning_point / turning_point_x_steps_from_previous_turning_point # slope / gradient
                    turning_point_slope_log_from_previous_turning_point = turning_point_y_log_distance_from_previous_turning_point / log_change_in_x # log slope / gradient
                    # market structure
                    turning_point_broke_structure_up = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0]) == 0 else 1 if turning_point > turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_High']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    turning_point_broke_structure_down = 0 if len(np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0]) == 0 else 1 if turning_point < turning_points_dict['Turning_Point'][np.where(np.array(turning_points_dict['Turning_Point_Is_A_Low']) == 1)[0][-1]] else 0 # 0 if false, 1 if true
                    # turning point low compared to current candle's close
                    current_close_minus_turning_point = candle_close_1 - turning_point
                    current_close_turning_point_log_change = np.log(candle_close_1 / turning_point)
                    current_close_minus_turning_point_close = candle_close_1 - turning_point_close
                    current_close_turning_point_close_log_change = np.log(candle_close_1 / turning_point_close)
                    # turning point low compared to current candle's open
                    current_open_minus_turning_point = candle_open_1 - turning_point
                    current_open_turning_point_log_change = np.log(candle_open_1 / turning_point)
                    current_open_minus_turning_point_close = candle_open_1 - turning_point_close
                    current_open_turning_point_close_log_change = np.log(candle_open_1 / turning_point_close)
                    # turning point low compared to current candle's high
                    current_high_minus_turning_point = candle_high_1 - turning_point
                    current_high_turning_point_log_change = np.log(candle_high_1 / turning_point)
                    current_high_minus_turning_point_close = candle_high_1 - turning_point_close
                    current_high_turning_point_close_log_change = np.log(candle_high_1 / turning_point_close)
                    # turning point low compared to current candle's low
                    current_low_minus_turning_point = candle_low_1 - turning_point
                    current_low_turning_point_log_change = np.log(candle_low_1 / turning_point)
                    current_low_minus_turning_point_close = candle_low_1 - turning_point_close
                    current_low_turning_point_close_log_change = np.log(candle_low_1 / turning_point_close)
                    # append parameter values to turning points dict
                    turning_points_dict['Turning_Point'].append(turning_point)
                    turning_points_dict['Turning_Point_Close'].append(turning_point_close)
                    turning_points_dict['Turning_Point_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_change_from_first_candle_close_in_view_window)
                    turning_points_dict['Turning_Point_Close_Change_From_First_Candle_Close_In_View_Window'].append(turning_point_close_change_from_first_candle_close_in_view_window)
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
                    turning_points_dict['Turning_Point_Subtracted_From_Current_Close'].append(current_close_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_Close'].append(current_close_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Close'].append(current_close_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Close'].append(current_close_turning_point_close_log_change)
                    turning_points_dict['Turning_Point_Subtracted_From_Current_Open'].append(current_open_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_Open'].append(current_open_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Open'].append(current_open_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Open'].append(current_open_turning_point_close_log_change)
                    turning_points_dict['Turning_Point_Subtracted_From_Current_High'].append(current_high_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_High'].append(current_high_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_High'].append(current_high_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_High'].append(current_high_turning_point_close_log_change)
                    turning_points_dict['Turning_Point_Subtracted_From_Current_Low'].append(current_low_minus_turning_point)
                    turning_points_dict['Turning_Point_Log_Change_From_Current_Low'].append(current_low_turning_point_log_change)
                    turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Low'].append(current_low_minus_turning_point_close)
                    turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Low'].append(current_low_turning_point_close_log_change)
            # ***********************************************************************************************
            # *********************************************************************************************************

            # calculations ********************************************************************************************
            # ohlc data's change from first candle in the view window
            _Open_Change_From_First_Candle_Close_In_View_Window = candle_open_1 - first_candle_close_in_view_window
            _High_Change_From_First_Candle_Close_In_View_Window = candle_high_1 - first_candle_close_in_view_window
            _Low_Change_From_First_Candle_Close_In_View_Window = candle_low_1 - first_candle_close_in_view_window
            _Close_Change_From_First_Candle_Close_In_View_Window = candle_close_1 - first_candle_close_in_view_window
            # ohlc data's log change from first candle in the view window
            _Open_Log_Change_From_First_Candle_Close_In_View_Window = np.log(candle_open_1 / first_candle_close_in_view_window)
            _High_Log_Change_From_First_Candle_Close_In_View_Window = np.log(candle_high_1 / first_candle_close_in_view_window)
            _Low_Log_Change_From_First_Candle_Close_In_View_Window = np.log(candle_low_1 / first_candle_close_in_view_window)
            _Close_Log_Change_From_First_Candle_Close_In_View_Window = np.log(candle_close_1 / first_candle_close_in_view_window)
            # candlestick types
            _Bullish = 1 if candle_close_1 > candle_close_1 else 0
            _Bearish = 1 if candle_close_1 < candle_open_1 else 0
            _Doji = 1 if candle_close_1 == candle_open_1 else 0
            # wicks
            _Upper_Wick = candle_high_1 - candle_close_1 if candle_close_1 >= candle_open_1 else candle_high_1 - candle_open_1
            _Lower_Wick = candle_close_1 - candle_low_1 if candle_close_1 < candle_open_1 else candle_open_1 - candle_low_1
            # wicks logs
            _Upper_Wick_Log = np.log(candle_high_1 / candle_close_1) if candle_close_1 >= candle_open_1 else np.log(candle_high_1 / candle_open_1)
            _Lower_Wick_Log = np.log(candle_close_1 / candle_low_1) if candle_close_1 < candle_open_1 else np.log(candle_open_1 / candle_low_1)
            # body size
            _Body_Size = candle_close_1 - candle_open_1
            # body size logs
            _Body_Size_Log = np.log(candle_close_1 / candle_open_1)
            # candlestick size
            _Candlestick_Size = candle_high_1 - candle_low_1
            # candlestick size logs
            _Candlestick_Size_Log = np.log(candle_high_1 / candle_low_1)
            # candlestick patterns **************************************************************************
            if candlestick_patterns_on == True:
                _Bearish_Harami = 1 if ((candle_close_2 > candle_open_2) and (candle_close_1 < candle_open_1) and (candle_close_1 > candle_open_2) and (candle_open_1 < candle_close_2)) else 0
                _Bearish_Harami_Cross = 1 if ((candle_close_2 > candle_open_2) and (candle_close_1 == candle_open_1) and (candle_close_1 > candle_open_2) and (candle_open_1 < candle_close_2)) else 0
                _Bearish_3_Method_Formation = 1 if ((candle_close_5 < candle_open_5) and (candle_close_4 > candle_open_4) and (candle_close_5 < candle_open_4) and (candle_open_5 > candle_close_4) and (candle_close_3 > candle_open_3) and (candle_close_5 < candle_open_3) and (candle_open_5 > candle_close_3) and (candle_close_2 > candle_open_2) and (candle_close_5 < candle_open_2) and (candle_open_5 > candle_close_2) and (candle_close_1 < candle_open_1) and (candle_close_1 < candle_open_2)) else 0
                _Bullish_3_Method_Formation = 1 if ((candle_close_5 > candle_open_5) and (candle_close_4 < candle_open_4) and (candle_close_5 > candle_open_4) and (candle_open_5 < candle_close_4) and (candle_close_3 < candle_open_3) and (candle_close_5 > candle_open_3) and (candle_open_5 < candle_close_3) and (candle_close_2 < candle_open_2) and (candle_close_5 > candle_open_2) and (candle_open_5 > candle_close_2) and (candle_close_1 > candle_open_1) and (candle_close_1 > candle_open_2)) else 0
                _Bullish_Harami = 1 if ((candle_close_2 < candle_open_2) and (candle_close_1 > candle_open_1) and (candle_close_2 < candle_open_1) and (candle_open_2 > candle_close_1)) else 0
                _Bullish_Harami_Cross = 1 if ((candle_close_2 < candle_open_2) and (candle_close_1 == candle_open_1) and (candle_close_2 < candle_open_1) and (candle_open_2 > candle_close_1)) else 0
                _Dark_Cloud_Cover = 1 if ((candle_close_2 > candle_open_2) and (candle_close_1 < candle_open_1) and (candle_high_2 < candle_open_1) and (candle_close_2 > candle_close_1) and (candle_open_2 < candle_close_1)) else 0
                _Engulfing_Bearish_Line = 1 if ((candle_close_2 > candle_open_2) and (candle_close_1 < candle_open_1) and (candle_close_2 < candle_open_1) and (candle_open_2 > candle_close_1)) else 0
                _Engulfing_Bullish_Line = 1 if ((candle_close_2 < candle_open_2) and (candle_close_1 > candle_open_1) and (candle_open_2 < candle_close_1) and (candle_close_2 > candle_open_1)) else 0
                _Evening_Doji_Star = 1 if ((candle_close_3 > candle_open_3) and (candle_close_2 == candle_open_2) and (candle_high_3 < candle_open_2) and (candle_close_1 < candle_open_1) and (candle_close_3 > candle_close_1)) else 0
                _Evening_Star = 1 if ((candle_close_3 > candle_open_3) and (candle_close_2 != candle_open_2) and (candle_high_3 < candle_open_2) and (candle_close_1 < candle_open_1) and (candle_close_3 > candle_close_1)) else 0
                _Falling_Window = 1 if (candle_low_2 > candle_high_1) else 0
                _Morning_Doji_Star = 1 if ((candle_close_3 < candle_open_3) and (candle_close_2 == candle_open_2) and (candle_low_3 > candle_close_2) and (candle_close_1 > candle_open_1) and (candle_close_3 < candle_close_1)) else 0
                _Morning_Star = 1 if ((candle_close_3 < candle_open_3) and (candle_close_2 != candle_open_2) and (candle_low_3 > candle_close_2) and (candle_close_1 > candle_open_1) and (candle_close_3 < candle_close_1)) else 0
                _On_Neckline = 1 if ((candle_close_2 < candle_open_2) and (candle_close_1 > candle_open_1) and (candle_low_2 < candle_close_1) and (candle_close_2 > candle_close_1)) else 0
                _Three_Black_Crows = 1 if ((candle_close_3 < candle_open_3) and (candle_close_2 < candle_open_2) and (candle_close_3 > candle_close_2) and (candle_close_1 < candle_open_1) and (candle_close_2 > candle_close_1)) else 0
                _Three_White_Soldiers = 1 if ((candle_close_3 > candle_open_3) and (candle_close_2 > candle_open_2) and (candle_close_3 < candle_close_2) and (candle_close_1 > candle_open_1) and (candle_close_2 < candle_close_1)) else 0
                _Tweezer_Bottoms = 1 if (candle_low_2 == candle_low_1) else 0
                _Tweezer_Tops = 1 if (candle_high_2 == candle_high_1) else 0
                _Doji_Star = 1 if ((candle_close_2 != candle_open_2) and (candle_close_1 == candle_open_1) and (candle_low_2 > candle_close_1)) else 0
                _Piercing_Line = 1 if ((candle_close_2 < candle_open_2) and (candle_close_1 > candle_open_1) and (candle_low_2 > candle_open_1) and (((candle_close_2 + candle_open_2) / 2) < candle_close_1)) else 0
                _Rising_Window = 1 if (candle_high_2 < candle_low_1) else 0
                # _Doji = 1 if (candle_close_1 == candle_open_1) else 0 # already done for candlestick type above  (bullish / bearish / doji)
                _Dragon_Fly_Doji = 1 if ((candle_close_1 == candle_open_1) and (candle_close_1 == candle_high_1) and (candle_high_1 != candle_low_1)) else 0
                _Gravestone_Doji = 1 if ((candle_close_1 == candle_open_1) and (candle_close_1 == candle_low_1) and (candle_high_1 != candle_low_1)) else 0
                _Hanging_Man = 1 if ((candle_close_1 != candle_open_1) and (abs(_Upper_Wick) <= abs(_Body_Size / 6)) and (abs(_Lower_Wick) >= abs(_Body_Size * 2))) else 0
                _Hammer = 1 if ((candle_close_1 != candle_open_1) and (abs(_Upper_Wick) <= abs(_Body_Size / 3)) and (abs(_Lower_Wick) >= abs(_Body_Size))) else 0
                _Inverted_Black_Hammer = 1 if ((candle_close_1 < candle_open_1) and (abs(_Lower_Wick) <= abs(_Body_Size / 3)) and (abs(_Upper_Wick) >= abs(_Body_Size))) else 0
                _Inverted_Hammer = 1 if ((candle_close_1 != candle_open_1) and (abs(_Lower_Wick) <= abs(_Body_Size / 3)) and (abs(_Upper_Wick) >= abs(_Body_Size))) else 0
                _Long_Lower_Shadow = 1 if ((candle_close_1 != candle_open_1) and (abs(_Lower_Wick) >= abs((2/3) * _Candlestick_Size))) else 0
                _Long_Upper_Shadow = 1 if ((candle_close_1 != candle_open_1) and (abs(_Upper_Wick) >= abs((2/3) * _Candlestick_Size))) else 0
                _Marubozu = 1 if ((candle_close_1 != candle_open_1) and (_Upper_Wick == 0) and (_Lower_Wick == 0)) else 0
                _Shooting_Star = 1 if ((candle_close_1 != candle_open_1) and (abs(_Lower_Wick) <= abs(_Body_Size / 6)) and (abs(_Upper_Wick) >= abs(_Body_Size * 2))) else 0
                _Shaven_Bottom = 1 if ((candle_close_1 != candle_open_1) and (_Lower_Wick == 0) and (_Upper_Wick != 0)) else 0
                _Shaven_Head = 1 if ((candle_close_1 != candle_open_1) and (_Lower_Wick != 0) and (_Upper_Wick == 0)) else 0
            # ***********************************************************************************************
            # MAs *******************************************************************************************
            for ma_type in ma_types:
                # periods
                if ma_type == 'Simple': periods = sma_periods; ma_function = calculate_simple_ma
                elif ma_type == 'Exponential': periods = ema_periods; ma_function = calculate_exponential_ma
                elif ma_type == 'Smoothed': periods = smoothed_periods; ma_function = calculate_smoothed_ma
                elif ma_type == 'Weighted': periods = weighted_periods; ma_function = calculate_weighted_ma

                # larger ma calculation function
                if larger_ma_type == 'Simple': larger_ma_function = calculate_simple_ma
                elif larger_ma_type == 'Exponential': larger_ma_function = calculate_exponential_ma
                elif larger_ma_type == 'Smoothed': larger_ma_function = calculate_smoothed_ma
                elif larger_ma_type == 'Weighted': larger_ma_function = calculate_weighted_ma
                elif larger_ma_type == 'Default': larger_ma_function = ma_function

                for z in range(len(periods)):
                    # period
                    period = periods[z]
                    # MA **************************************************************************
                    ma = ma_function(all_closes_till_i[-period:], period=period)
                    # add to df dict according to timeframe's append frequency
                    for k in range(append_frequency):
                        x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA'].append(ma)
                    # *****************************************************************************
                    # ma deep features*************************************************************
                    if ma_deep_features == True:
                        # MA change from first candle close in view window **************
                        ma_change_from_first_candle_close_in_view_window = ma - first_candle_close_in_view_window
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA_Change_From_First_Candle_Close_In_View_Window'].append(ma_change_from_first_candle_close_in_view_window)
                        # ***************************************************************
                        # MA log change from first candle close in view window **********
                        ma_log_change_from_first_candle_close_in_view_window = np.log(ma / first_candle_close_in_view_window)
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA_Log_Change_From_First_Candle_Close_In_View_Window'].append(ma_log_change_from_first_candle_close_in_view_window)
                        # ***************************************************************
                        # current close - MA ********************************************
                        current_close_minus_ma = candle_close_1 - ma
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_Close-'+str(period)+'_'+ma_type+'_MA'].append(current_close_minus_ma)
                        # ***************************************************************
                        # MA log change from current close ******************************
                        ma_log_change_from_current_close = np.log(candle_close_1 / ma)
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_Close_'+str(period)+'_'+ma_type+'_MA_Log_Change'].append(ma_log_change_from_current_close)
                        # ***************************************************************
                        # current open - MA *********************************************
                        current_open_minus_ma = candle_open_1 - ma
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_Open-'+str(period)+'_'+ma_type+'_MA'].append(current_open_minus_ma)
                        # ***************************************************************
                        # MA log change from current open *******************************
                        ma_log_change_from_current_open = np.log(candle_open_1 / ma)
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_Open_'+str(period)+'_'+ma_type+'_MA_Log_Change'].append(ma_log_change_from_current_open)
                        # ***************************************************************
                        # current high - MA *********************************************
                        current_high_minus_ma = candle_high_1 - ma
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_High-'+str(period)+'_'+ma_type+'_MA'].append(current_high_minus_ma)
                        # ***************************************************************
                        # MA log change from current high *******************************
                        ma_log_change_from_current_high = np.log(candle_high_1 / ma)
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_High_'+str(period)+'_'+ma_type+'_MA_Log_Change'].append(ma_log_change_from_current_high)
                        # ***************************************************************
                        # current low - MA **********************************************
                        current_low_minus_ma = candle_low_1 - ma
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_Low-'+str(period)+'_'+ma_type+'_MA'].append(current_low_minus_ma)
                        # ***************************************************************
                        # MA log change from current low ********************************
                        ma_log_change_from_current_low = np.log(candle_low_1 / ma)
                        # add to df dict according to timeframe's append frequency
                        for k in range(append_frequency):
                            x_dict[timeframe+'_Low_'+str(period)+'_'+ma_type+'_MA_Log_Change'].append(ma_log_change_from_current_low)
                        # ***************************************************************
                        # difference between current MA and every other MA before it ****
                        if z != 0:
                            for y in range(len(periods[:z])):
                                # larger MA period
                                larger_period = periods[y]
                                # larger MA
                                larger_ma = larger_ma_function(all_closes_till_i[-larger_period:], period=larger_period)
                                # current MA - larger MA **********************
                                current_ma_minus_larger_ma = ma - larger_ma
                                # add to df dict according to timeframe's append frequency
                                for k in range(append_frequency):
                                    x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA-'+str(larger_period)+'_'+ma_type+'_MA'].append(current_ma_minus_larger_ma)
                                # *********************************************
                                # current MA larger MA Log change *************
                                current_ma_larger_ma_log_change = np.log(ma / larger_ma)
                                # add to df dict according to timeframe's append frequency
                                for k in range(append_frequency):
                                    x_dict[timeframe+'_'+str(period)+'_'+ma_type+'_MA_'+str(larger_period)+'_'+ma_type+'_MA_Log_Change'].append(current_ma_larger_ma_log_change)
                                # *********************************************
                        # ***************************************************************
                    # *****************************************************************************
            # ***********************************************************************************************
            # RSIs ******************************************************************************************
            for period in rsi_periods:
                # period rsi
                rsi = calculate_rsi(closes[i-28:i+1], period=period)
                # add to df dict according to timeframe's append frequency
                for k in range(append_frequency):
                    x_dict[timeframe+'_'+str(period)+'_Period_RSI'].append(rsi)
            # ***********************************************************************************************
            # typical prices ********************************************************************************
            typical_prices = calculate_typical_price(closes[i-28:i+1], opens[i-28:i+1], highs[i-28:i+1], lows[i-28:i+1])
            # ***********************************************************************************************
            # standard deviations ***************************************************************************
            for period in std_periods:
                # period standard deviation
                rolling_std = calculate_rolling_std(typical_prices, period=period)
                # add to df dict according to timeframe's append frequency
                for k in range(append_frequency):
                    x_dict[timeframe+'_'+str(period)+'_Period_Std'].append(rolling_std)
            # ***********************************************************************************************
            # ichimoku kinko hyo ****************************************************************************
            if ichimoku_on == True:
                # obtain ichimoku indicator values
                tenkan_sen, kijun_sen, chikou_span, senkou_span_a, senkou_span_b = calculate_ichimoku_kinko_hyo(highs[i-55:i+1], lows[i-55:i+1], closes[i-55:i+1])
                # obtain old ichimoku indicator values (from 26 periods back)
                old_tenkan_sen, old_kijun_sen, old_chikou_span, old_senkou_span_a, old_senkou_span_b = calculate_ichimoku_kinko_hyo(highs[i-81:i-26+1], lows[i-81:i-26+1], closes[i-81:i-26+1])
                # calculations ********************************************************************
                # tenkan-sen ************************************************************
                # tenkan-sen value
                _Tenkan_sen = tenkan_sen
                # ichimoku deep features **************************************
                if ichimoku_deep_feature_comparison == True:
                    # change from first candle close in view window
                    _Tenkan_sen_Change_From_First_Candle_Close_In_View_Window = tenkan_sen - first_candle_close_in_view_window
                    # log change from first candle close in view window
                    _Tenkan_sen_Log_Change_From_First_Candle_Close_In_View_Window = np.log(tenkan_sen / first_candle_close_in_view_window)
                    # current close - tenkan-sen
                    _Current_Close_Minus_Tenkan_sen = candle_close_1 - tenkan_sen
                    # tenkan-sen log change from current close
                    _Close_Tenkan_sen_Log_Change = np.log(candle_close_1 / tenkan_sen)
                    # current open - tenkan-sen
                    _Open_Minus_Tenkan_sen = candle_open_1 - tenkan_sen
                    # tenkan-sen log change from current open
                    _Open_Tenkan_sen_Log_Change = np.log(candle_open_1 / tenkan_sen)
                    # current high - tenkan-sen
                    _Current_High_Minus_Tenkan_sen = candle_high_1 - tenkan_sen
                    # tenkan-sen log change from current high
                    _High_Tenkan_sen_Log_Change = np.log(candle_high_1 / tenkan_sen)
                    # current low - tenkan-sen
                    _Low_Minus_Tenkan_sen = candle_low_1 - tenkan_sen
                    # tenkan-sen log change from current low
                    _Low_Tenkan_sen_Log_Change = np.log(candle_low_1 / tenkan_sen)
                    # ichimoku own feature comparison ***************
                    if ichimoku_own_feature_comparison == True:
                        # tenkan-sen - kijun-sen
                        _Tenkan_sen_Minus_Kijun_sen = tenkan_sen - kijun_sen
                        # tenkan-sen log change from kijun-sen
                        _Tenkan_sen_Kijun_sen_Log_Change = np.log(tenkan_sen / kijun_sen)
                    # ***********************************************
                # *************************************************************
                # ***********************************************************************
                # kijun-sen *************************************************************
                # kijun-sen value
                _Kijun_sen = kijun_sen
                # ichimoku deep features **************************************
                if ichimoku_deep_feature_comparison == True:
                    # change from first candle close in view window
                    _Kijun_sen_Change_From_First_Candle_Close_In_View_Window = kijun_sen - first_candle_close_in_view_window
                    # log change from first candle close in view window
                    _Kijun_sen_Log_Change_From_First_Candle_Close_In_View_Window = np.log(kijun_sen / first_candle_close_in_view_window)
                    # current close - kijun-sen
                    _Current_Close_Minus_Kijun_sen = candle_close_1 - kijun_sen
                    # kijun-sen log change from current close
                    _Close_Kijun_sen_Log_Change = np.log(candle_close_1 / kijun_sen)
                    # current open - kijun-sen
                    _Open_Minus_Kijun_sen = candle_open_1 - kijun_sen
                    # kijun-sen log change from current open
                    _Open_Kijun_sen_Log_Change = np.log(candle_open_1 / kijun_sen)
                    # current high - kijun-sen
                    _High_Minus_Kijun_sen = candle_high_1 - kijun_sen
                    # kijun-sen log change from current high
                    _High_Kijun_sen_Log_Change = np.log(candle_high_1 / kijun_sen)
                    # current low - kijun-sen
                    _Low_Minus_Kijun_sen = candle_low_1 - kijun_sen
                    # kijun-sen log change from current low
                    _Low_Kijun_sen_Log_Change = np.log(candle_low_1 / kijun_sen)
                # *************************************************************
                # ***********************************************************************
                # chikou span ***********************************************************
                # chikou span value
                _Chikou_Span = chikou_span
                # senkou span a (from 26 periods back) - chikou span
                _Senkou_Span_A_Minus_Chikou_Span = old_senkou_span_a - chikou_span
                # chikou span log change from senkou span a (from 26 periods back)
                _Senkou_Span_A_Chikou_Span_Log_Change = np.log(old_senkou_span_a / chikou_span)
                # senkou span b (from 26 periods back) - chikou span
                _Senkou_Span_B_Minus_Chikou_Span = old_senkou_span_b - chikou_span
                # chikou span log change from senkou span b (from 26 periods back)
                _Senkou_Span_B_Chikou_Span_Log_Change = np.log(old_senkou_span_b / chikou_span)
                # ***********************************************************************
                # senkou span a *********************************************************
                # senkou span a value
                _Senkou_Span_A = senkou_span_a
                # ichimoku deep features **************************************
                if ichimoku_deep_feature_comparison == True:
                    # change from first candle close in view window
                    _Senkou_Span_A_Change_From_First_Candle_Close_In_View_Window = senkou_span_a - first_candle_close_in_view_window
                    # log change from first candle close in view window
                    _Senkou_Span_A_Log_Change_From_First_Candle_Close_In_View_Window = np.log(senkou_span_a / first_candle_close_in_view_window)
                    # current close - senkou span a
                    _Current_Close_Minus_Senkou_Span_A = candle_close_1 - senkou_span_a
                    # senkou span a log change from current close
                    _Close_Senkou_Span_A_Log_Change = np.log(candle_close_1 / senkou_span_a)
                    # current open - senkou span a
                    _Open_Minus_Senkou_Span_A = candle_open_1 - senkou_span_a
                    # senkou span a log change from current open
                    _Open_Senkou_Span_A_Log_Change = np.log(candle_open_1 / senkou_span_a)
                    # current high - senkou span a
                    _High_Minus_Senkou_Span_A = candle_high_1 - senkou_span_a
                    # senkou span a log change from current high
                    _High_Senkou_Span_A_Log_Change = np.log(candle_high_1 / senkou_span_a)
                    # current low - senkou span a
                    _Low_Minus_Senkou_Span_A = candle_low_1 - senkou_span_a
                    # senkou span a log change from current low
                    _Low_Senkou_Span_A_Log_Change = np.log(candle_low_1 / senkou_span_a)
                    # ichimoku own feature comparison ***************
                    if ichimoku_own_feature_comparison == True:
                        # senkou span a - senkou span b
                        _Senkou_Span_A_Minus_Senkou_Span_B = senkou_span_a - senkou_span_b
                        # senkou span a log change from senkou span b
                        _Senkou_Span_A_Senkou_Span_B_Log_Change = np.log(senkou_span_a / senkou_span_b)
                    # ***********************************************
                # *************************************************************
                # ***********************************************************************
                # senkou span b *********************************************************
                # senkou span b value
                _Senkou_Span_B = senkou_span_b
                # ichimoku deep features **************************************
                if ichimoku_deep_feature_comparison == True:
                    # change from first candle close in view window
                    _Senkou_Span_B_Change_From_First_Candle_Close_In_View_Window = senkou_span_b - first_candle_close_in_view_window
                    # log change from first candle close in view window
                    _Senkou_Span_B_Log_Change_From_First_Candle_Close_In_View_Window = np.log(senkou_span_b / first_candle_close_in_view_window)
                    # current close - senkou span b
                    _Current_Close_Minus_Senkou_Span_B = candle_close_1 - senkou_span_b
                    # senkou span b log change from current close
                    _Close_Senkou_Span_B_Log_Change = np.log(candle_close_1 / senkou_span_b)
                    # current open - senkou span b
                    _Open_Minus_Senkou_Span_B = candle_open_1 - senkou_span_b
                    # senkou span b log change from current open
                    _Open_Senkou_Span_B_Log_Change = np.log(candle_open_1 / senkou_span_b)
                    # current high - senkou span b
                    _High_Minus_Senkou_Span_B = candle_high_1 - senkou_span_b
                    # senkou span b log change from current high
                    _High_Senkou_Span_B_Log_Change = np.log(candle_high_1 / senkou_span_b)
                    # current low - senkou span b
                    _Low_Minus_Senkou_Span_B = candle_low_1 - senkou_span_b
                    # senkou span b log change from current low
                    _Low_Senkou_Span_B_Log_Change = np.log(candle_low_1 / senkou_span_b)
                # *************************************************************
                # ***********************************************************************
                # *********************************************************************************
                # add to df dict according to timeframe's append frequency ************************
                for k in range(append_frequency):
                    # tenkan-sen ********************************************************
                    # tenkan-sen values
                    x_dict[timeframe+'_Tenkan-sen'].append(_Tenkan_sen)
                    # ichimoku deep features **********************************
                    if ichimoku_deep_feature_comparison == True:
                        # change from first candle close in view window
                        x_dict[timeframe+'_Tenkan-sen_Change_From_First_Candle_Close_In_View_Window'].append(_Tenkan_sen_Change_From_First_Candle_Close_In_View_Window)
                        # log change from first candle close in view window
                        x_dict[timeframe+'_Tenkan-sen_Log_Change_From_First_Candle_Close_In_View_Window'].append(_Tenkan_sen_Log_Change_From_First_Candle_Close_In_View_Window)
                        # current close - tenkan-sen
                        x_dict[timeframe+'_Current_Close-Tenkan-sen'].append(_Current_Close_Minus_Tenkan_sen)
                        # tenkan-sen log change from current close
                        x_dict[timeframe+'_Close_Tenkan-sen_Log_Change'].append(_Close_Tenkan_sen_Log_Change)
                        # current open - tenkan-sen
                        x_dict[timeframe+'_Open-Tenkan-sen'].append(_Open_Minus_Tenkan_sen)
                        # tenkan-sen log change from current open
                        x_dict[timeframe+'_Open_Tenkan-sen_Log_Change'].append(_Open_Tenkan_sen_Log_Change)
                        # current high - tenkan-sen
                        x_dict[timeframe+'_High-Tenkan-sen'].append(_Current_High_Minus_Tenkan_sen)
                        # tenkan-sen log change from current high
                        x_dict[timeframe+'_High_Tenkan-sen_Log_Change'].append(_High_Tenkan_sen_Log_Change)
                        # current low - tenkan-sen
                        x_dict[timeframe+'_Low-Tenkan-sen'].append(_Low_Minus_Tenkan_sen)
                        # tenkan-sen log change from current low
                        x_dict[timeframe+'_Low_Tenkan-sen_Log_Change'].append(_Low_Tenkan_sen_Log_Change)
                        # ichimoku own feature comparison ***********
                        if ichimoku_own_feature_comparison == True:
                            # tenkan-sen - kijun-sen
                            x_dict[timeframe+'_Tenkan-sen-Kijun-sen'].append(_Tenkan_sen_Minus_Kijun_sen)
                            # tenkan-sen log change from kijun-sen
                            x_dict[timeframe+'_Tenkan-sen_Kijun-sen_Log_Change'].append(_Tenkan_sen_Kijun_sen_Log_Change)
                        # *******************************************
                    # *********************************************************
                    # *******************************************************************
                    # kijun-sen *********************************************************
                    # kijun-sen values
                    x_dict[timeframe+'_Kijun-sen'].append(_Kijun_sen)
                    # ichimoku deep features **********************************
                    if ichimoku_deep_feature_comparison == True:
                        # change from first candle close in view window
                        x_dict[timeframe+'_Kijun-sen_Change_From_First_Candle_Close_In_View_Window'].append(_Kijun_sen_Change_From_First_Candle_Close_In_View_Window)
                        # log change from first candle close in view window
                        x_dict[timeframe+'_Kijun-sen_Log_Change_From_First_Candle_Close_In_View_Window'].append(_Kijun_sen_Log_Change_From_First_Candle_Close_In_View_Window)
                        # current close - kijun-sen
                        x_dict[timeframe+'_Current_Close-Kijun-sen'].append(_Current_Close_Minus_Kijun_sen)
                        # kijun-sen log change from current close
                        x_dict[timeframe+'_Close_Kijun-sen_Log_Change'].append(_Close_Kijun_sen_Log_Change)
                        # current open - kijun-sen
                        x_dict[timeframe+'_Open-Kijun-sen'].append(_Open_Minus_Kijun_sen)
                        # kijun-sen log change from current open
                        x_dict[timeframe+'_Open_Kijun-sen_Log_Change'].append(_Open_Kijun_sen_Log_Change)
                        # current high - kijun-sen
                        x_dict[timeframe+'_High-Kijun-sen'].append(_High_Minus_Kijun_sen)
                        # kijun-sen log change from current high
                        x_dict[timeframe+'_High_Kijun-sen_Log_Change'].append(_High_Kijun_sen_Log_Change)
                        # current low - kijun-sen
                        x_dict[timeframe+'_Low-Kijun-sen'].append(_Low_Minus_Kijun_sen)
                        # kijun-sen log change from current low
                        x_dict[timeframe+'_Low_Kijun-sen_Log_Change'].append(_Low_Kijun_sen_Log_Change)
                    # *********************************************************
                    # *******************************************************************
                    # chikou span *******************************************************
                    # chikou span values
                    x_dict[timeframe+'_Chikou_Span'].append(_Chikou_Span)
                    # senkou span a (from 26 periods back) - chikou span
                    x_dict[timeframe+'_Senkou_Span_A-Chikou_Span'].append(_Senkou_Span_A_Minus_Chikou_Span)
                    # chikou span log change from senkou span a (from 26 periods back)
                    x_dict[timeframe+'_Senkou_Span_A_Chikou_Span_Log_Change'].append(_Senkou_Span_A_Chikou_Span_Log_Change)
                    # senkou span b (from 26 periods back) - chikou span
                    x_dict[timeframe+'_Senkou_Span_B-Chikou_Span'].append(_Senkou_Span_B_Minus_Chikou_Span)
                    # chikou span log change from senkou span b (from 26 periods back)
                    x_dict[timeframe+'_Senkou_Span_B_Chikou_Span_Log_Change'].append(_Senkou_Span_B_Chikou_Span_Log_Change)
                    # *******************************************************************
                    # senkou span a *****************************************************
                    # senkou span a values
                    x_dict[timeframe+'_Senkou_Span_A'].append(_Senkou_Span_A)
                    # ichimoku deep features **********************************
                    if ichimoku_deep_feature_comparison == True:
                        # change from first candle close in view window
                        x_dict[timeframe+'_Senkou_Span_A_Change_From_First_Candle_Close_In_View_Window'].append(_Senkou_Span_A_Change_From_First_Candle_Close_In_View_Window)
                        # log change from first candle close in view window
                        x_dict[timeframe+'_Senkou_Span_A_Log_Change_From_First_Candle_Close_In_View_Window'].append(_Senkou_Span_A_Log_Change_From_First_Candle_Close_In_View_Window)
                        # current close - senkou span a
                        x_dict[timeframe+'_Current_Close-Senkou_Span_A'].append(_Current_Close_Minus_Senkou_Span_A)
                        # senkou span a log change from current close
                        x_dict[timeframe+'_Close_Senkou_Span_A_Log_Change'].append(_Close_Senkou_Span_A_Log_Change)
                        # current open - senkou span a
                        x_dict[timeframe+'_Open-Senkou_Span_A'].append(_Open_Minus_Senkou_Span_A)
                        # senkou span a log change from current open
                        x_dict[timeframe+'_Open_Senkou_Span_A_Log_Change'].append(_Open_Senkou_Span_A_Log_Change)
                        # current high - senkou span a
                        x_dict[timeframe+'_High-Senkou_Span_A'].append(_High_Minus_Senkou_Span_A)
                        # senkou span a log change from current high
                        x_dict[timeframe+'_High_Senkou_Span_A_Log_Change'].append(_High_Senkou_Span_A_Log_Change)
                        # current low - senkou span a
                        x_dict[timeframe+'_Low-Senkou_Span_A'].append(_Low_Minus_Senkou_Span_A)
                        # senkou span a log change from current low
                        x_dict[timeframe+'_Low_Senkou_Span_A_Log_Change'].append(_Low_Senkou_Span_A_Log_Change)
                        # ichimoku own feature comparison ***********
                        if ichimoku_own_feature_comparison == True:
                            # senkou span a - senkou span b
                            x_dict[timeframe+'_Senkou_Span_A-Senkou_Span_B'].append(_Senkou_Span_A_Minus_Senkou_Span_B)
                            # senkou span a log change from senkou span b
                            x_dict[timeframe+'_Senkou_Span_A_Senkou_Span_B_Log_Change'].append(_Senkou_Span_A_Senkou_Span_B_Log_Change)
                        # *******************************************
                    # *********************************************************
                    # *******************************************************************
                    # senkou span b *****************************************************
                    # senkou span b values
                    x_dict[timeframe+'_Senkou_Span_B'].append(_Senkou_Span_B)
                    # ichimoku deep features **********************************
                    if ichimoku_deep_feature_comparison == True:
                        # change from first candle close in view window
                        x_dict[timeframe+'_Senkou_Span_B_Change_From_First_Candle_Close_In_View_Window'].append(_Senkou_Span_B_Change_From_First_Candle_Close_In_View_Window)
                        # log change from first candle close in view window
                        x_dict[timeframe+'_Senkou_Span_B_Log_Change_From_First_Candle_Close_In_View_Window'].append(_Senkou_Span_B_Log_Change_From_First_Candle_Close_In_View_Window)
                        # current close - senkou span b
                        x_dict[timeframe+'_Current_Close-Senkou_Span_B'].append(_Current_Close_Minus_Senkou_Span_B)
                        # senkou span b log change from current close
                        x_dict[timeframe+'_Close_Senkou_Span_B_Log_Change'].append(_Close_Senkou_Span_B_Log_Change)
                        # current open - senkou span b
                        x_dict[timeframe+'_Open-Senkou_Span_B'].append(_Open_Minus_Senkou_Span_B)
                        # senkou span b log change from current open
                        x_dict[timeframe+'_Open_Senkou_Span_B_Log_Change'].append(_Open_Senkou_Span_B_Log_Change)
                        # current high - senkou span b
                        x_dict[timeframe+'_High-Senkou_Span_B'].append(_High_Minus_Senkou_Span_B)
                        # senkou span b log change from current high
                        x_dict[timeframe+'_High_Senkou_Span_B_Log_Change'].append(_High_Senkou_Span_B_Log_Change)
                        # current low - senkou span b
                        x_dict[timeframe+'_Low-Senkou_Span_B'].append(_Low_Minus_Senkou_Span_B)
                        # senkou span b log change from current low
                        x_dict[timeframe+'_Low_Senkou_Span_B_Log_Change'].append(_Low_Senkou_Span_B_Log_Change)
                    # *********************************************************
                    # *******************************************************************
                # *********************************************************************************
            # ***********************************************************************************************
            # *********************************************************************************************************
            # populate df dict according to timeframe's append frequency **********************************************
            for k in range(append_frequency):
                # timestamp
                x_dict[timeframe+'_Timestamp'].append(str(candle_date_1))
                # ohlc data
                x_dict[timeframe+'_Open'].append(candle_open_1)
                x_dict[timeframe+'_High'].append(candle_high_1)
                x_dict[timeframe+'_Low'].append(candle_low_1)
                x_dict[timeframe+'_Close'].append(candle_close_1)
                # ohlc data's change from first candle in the view window
                x_dict[timeframe+'_Open_Change_From_First_Candle_Close_In_View_Window'].append(_Open_Change_From_First_Candle_Close_In_View_Window)
                x_dict[timeframe+'_High_Change_From_First_Candle_Close_In_View_Window'].append(_High_Change_From_First_Candle_Close_In_View_Window)
                x_dict[timeframe+'_Low_Change_From_First_Candle_Close_In_View_Window'].append(_Low_Change_From_First_Candle_Close_In_View_Window)
                x_dict[timeframe+'_Close_Change_From_First_Candle_Close_In_View_Window'].append(_Close_Change_From_First_Candle_Close_In_View_Window)
                # ohlc data's log change from first candle in the view window
                x_dict[timeframe+'_Open_Log_Change_From_First_Candle_Close_In_View_Window'].append(_Open_Log_Change_From_First_Candle_Close_In_View_Window)
                x_dict[timeframe+'_High_Log_Change_From_First_Candle_Close_In_View_Window'].append(_High_Log_Change_From_First_Candle_Close_In_View_Window)
                x_dict[timeframe+'_Low_Log_Change_From_First_Candle_Close_In_View_Window'].append(_Low_Log_Change_From_First_Candle_Close_In_View_Window)
                x_dict[timeframe+'_Close_Log_Change_From_First_Candle_Close_In_View_Window'].append(_Close_Log_Change_From_First_Candle_Close_In_View_Window)
                # candlestick types
                x_dict[timeframe+'_Bullish'].append(_Bullish)
                x_dict[timeframe+'_Bearish'].append(_Bearish)
                x_dict[timeframe+'_Doji'].append(_Doji)
                # wicks
                x_dict[timeframe+'_Upper_Wick'].append(_Upper_Wick)
                x_dict[timeframe+'_Lower_Wick'].append(_Lower_Wick)
                # wicks logs
                x_dict[timeframe+'_Upper_Wick_Log'].append(_Upper_Wick_Log)
                x_dict[timeframe+'_Lower_Wick_Log'].append(_Lower_Wick_Log)
                # body size
                x_dict[timeframe+'_Body_Size'].append(_Body_Size)
                # body size logs
                x_dict[timeframe+'_Body_Size_Log'].append(_Body_Size_Log)
                # candlestick size
                x_dict[timeframe+'_Candlestick_Size'].append(_Candlestick_Size)
                # candlestick size logs
                x_dict[timeframe+'_Candlestick_Size_Log'].append(_Candlestick_Size_Log)
                # candlestick patterns **********************************************************************
                if candlestick_patterns_on == True:
                    x_dict[timeframe+'_Bearish_Harami'].append(_Bearish_Harami)
                    x_dict[timeframe+'_Bearish_Harami_Cross'].append(_Bearish_Harami_Cross)
                    x_dict[timeframe+'_Bearish_3_Method_Formation'].append(_Bearish_3_Method_Formation)
                    x_dict[timeframe+'_Bullish_3_Method_Formation'].append(_Bullish_3_Method_Formation)
                    x_dict[timeframe+'_Bullish_Harami'].append(_Bullish_Harami)
                    x_dict[timeframe+'_Bullish_Harami_Cross'].append(_Bullish_Harami_Cross)
                    x_dict[timeframe+'_Dark_Cloud_Cover'].append(_Dark_Cloud_Cover)
                    x_dict[timeframe+'_Engulfing_Bearish_Line'].append(_Engulfing_Bearish_Line)
                    x_dict[timeframe+'_Engulfing_Bullish_Line'].append(_Engulfing_Bullish_Line)
                    x_dict[timeframe+'_Evening_Doji_Star'].append(_Evening_Doji_Star)
                    x_dict[timeframe+'_Evening_Star'].append(_Evening_Star)
                    x_dict[timeframe+'_Falling_Window'].append(_Falling_Window)
                    x_dict[timeframe+'_Morning_Doji_Star'].append(_Morning_Doji_Star)
                    x_dict[timeframe+'_Morning_Star'].append(_Morning_Star)
                    x_dict[timeframe+'_On_Neckline'].append(_On_Neckline)
                    x_dict[timeframe+'_Three_Black_Crows'].append(_Three_Black_Crows)
                    x_dict[timeframe+'_Three_White_Soldiers'].append(_Three_White_Soldiers)
                    x_dict[timeframe+'_Tweezer_Bottoms'].append(_Tweezer_Bottoms)
                    x_dict[timeframe+'_Tweezer_Tops'].append(_Tweezer_Tops)
                    x_dict[timeframe+'_Doji_Star'].append(_Doji_Star)
                    x_dict[timeframe+'_Piercing_Line'].append(_Piercing_Line)
                    x_dict[timeframe+'_Rising_Window'].append(_Rising_Window)
                    # x_dict[timeframe+'_Doji'].append(_Doji) # already done for candlestick type above  (bullish / bearish / doji)
                    x_dict[timeframe+'_Dragon_Fly_Doji'].append(_Dragon_Fly_Doji)
                    x_dict[timeframe+'_Gravestone_Doji'].append(_Gravestone_Doji)
                    x_dict[timeframe+'_Hanging_Man'].append(_Hanging_Man)
                    x_dict[timeframe+'_Hammer'].append(_Hammer)
                    x_dict[timeframe+'_Inverted_Black_Hammer'].append(_Inverted_Black_Hammer)
                    x_dict[timeframe+'_Inverted_Hammer'].append(_Inverted_Hammer)
                    x_dict[timeframe+'_Long_Lower_Shadow'].append(_Long_Lower_Shadow)
                    x_dict[timeframe+'_Long_Upper_Shadow'].append(_Long_Upper_Shadow)
                    x_dict[timeframe+'_Marubozu'].append(_Marubozu)
                    x_dict[timeframe+'_Shooting_Star'].append(_Shooting_Star)
                    x_dict[timeframe+'_Shaven_Bottom'].append(_Shaven_Bottom)
                    x_dict[timeframe+'_Shaven_Head'].append(_Shaven_Head)
                # *******************************************************************************************
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
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Change_From_First_Candle_Close_In_View_Window'].append(turning_points_dict['Turning_Point_Change_From_First_Candle_Close_In_View_Window'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Change_From_First_Candle_Close_In_View_Window'].append(turning_points_dict['Turning_Point_Close_Change_From_First_Candle_Close_In_View_Window'][-j])
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
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_Close'].append(turning_points_dict['Turning_Point_Subtracted_From_Current_Close'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_Close'].append(turning_points_dict['Turning_Point_Log_Change_From_Current_Close'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_Close'].append(turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Close'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_Close'].append(turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Close'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_Open'].append(turning_points_dict['Turning_Point_Subtracted_From_Current_Open'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_Open'].append(turning_points_dict['Turning_Point_Log_Change_From_Current_Open'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_Open'].append(turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Open'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_Open'].append(turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Open'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_High'].append(turning_points_dict['Turning_Point_Subtracted_From_Current_High'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_High'].append(turning_points_dict['Turning_Point_Log_Change_From_Current_High'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_High'].append(turning_points_dict['Turning_Point_Close_Subtracted_From_Current_High'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_High'].append(turning_points_dict['Turning_Point_Close_Log_Change_From_Current_High'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Subtracted_From_Current_Low'].append(turning_points_dict['Turning_Point_Subtracted_From_Current_Low'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Log_Change_From_Current_Low'].append(turning_points_dict['Turning_Point_Log_Change_From_Current_Low'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Subtracted_From_Current_Low'].append(turning_points_dict['Turning_Point_Close_Subtracted_From_Current_Low'][-j])
                    x_dict[timeframe+'_'+position+'_Most_Recent_Turning_Point_Close_Log_Change_From_Current_Low'].append(turning_points_dict['Turning_Point_Close_Log_Change_From_Current_Low'][-j])
                # *******************************************************************************************
            # *********************************************************************************************************
        # ***********************************************************************************************************************
    # *************************************************************************************************************************************

    # cut all x_dict arrays to last n elements to match entry timeframe data **************************************************************
    # entry timeframe timestamps
    entry_timeframe_timestamps = np.array(x_dict[entry_timeframe+'_Timestamp'])
    # entry timeframe data length
    entry_timeframe_data_length = len(entry_timeframe_timestamps)
    # last entry timeframe timestamp
    last_entry_timeframe_timestamp = entry_timeframe_timestamps[-1]
    # last entry timeframe timestamp minus minutes
    last_entry_timeframe_timestamp_minus_minutes = str(last_entry_timeframe_timestamp)[:-2]
    # entry timeframe data indexes within entry timeframe last timestamp's hour
    entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_hour = np.where(entry_timeframe_timestamps >= last_entry_timeframe_timestamp_minus_minutes)[0]
    # number of entry timeframe data indexes within entry timeframe last timestamp's hour
    number_of_entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_hour = len(entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_hour)
    # last entry timeframe timestamp minus hours and minutes
    last_entry_timeframe_timestamp_minus_hours_and_minutes = str(last_entry_timeframe_timestamp)[:-6]
    # entry timeframe data indexes within entry timeframe last timestamp's day
    entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_day = np.where(entry_timeframe_timestamps >= last_entry_timeframe_timestamp_minus_hours_and_minutes)[0]
    # number of entry timeframe data indexes within entry timeframe last timestamp's day
    number_of_entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_day = len(entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_day)
    # initialialize splice indexes dict for each timeframe except the entry timeframe
    splice_indexes = {}
    for timeframe in timeframes:
        # if timeframe is not the entry timeframe
        if timeframe != entry_timeframe:
            # timestamp match limit index
            if timeframe == 'Daily':
                timestamp_match_limit_index = number_of_entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_day
            else:
                timestamp_match_limit_index = number_of_entry_timeframe_data_indexes_within_entry_timeframe_last_timestamp_hour 
            # current timeframe timestamps
            current_timeframe_timestamps = np.array(x_dict[timeframe+'_Timestamp'])
            # indexes of current timeframe timestamps within entry timeframe's timestamp timeline
            indexes_of_current_timeframe_timestamps_within_entry_timeframe_timestamp_timeline = np.where(current_timeframe_timestamps <= last_entry_timeframe_timestamp)[0]
            # current timeframe timestamps within entry timeframe's timestamp timeline
            current_timeframe_timestamps_within_entry_timeframe_timestamp_timeline =  current_timeframe_timestamps[indexes_of_current_timeframe_timestamps_within_entry_timeframe_timestamp_timeline]
            # last current timeframe's timestamp
            last_current_timeframe_timestamp = current_timeframe_timestamps_within_entry_timeframe_timestamp_timeline[-1]
            # last current timeframe's timestamp occurance indexes
            last_current_timeframe_timestamp_occurance_indexes = np.where(current_timeframe_timestamps_within_entry_timeframe_timestamp_timeline >= last_current_timeframe_timestamp)[0]
            # indexes of last current timeframe timestamp's frequency matched to last entry timeframe timestamp's frequency
            indexes_of_last_current_timeframe_timestamp_frequency_matched_to_last_entry_timeframe_timestamp_frequency = last_current_timeframe_timestamp_occurance_indexes[:timestamp_match_limit_index]
            # original last current timeframe data index
            original_last_current_timeframe_data_index = len(current_timeframe_timestamps) - 1
            # corrected last current timeframe data index
            corrected_last_current_timeframe_data_index = indexes_of_last_current_timeframe_timestamp_frequency_matched_to_last_entry_timeframe_timestamp_frequency[-1]
            # index difference
            index_difference = original_last_current_timeframe_data_index - corrected_last_current_timeframe_data_index
            # timeframe splice start index
            timeframe_splice_start_index = -entry_timeframe_data_length - abs(index_difference)
            # timeframe splice stop index 
            timeframe_splice_stop_index = corrected_last_current_timeframe_data_index + 1 # +1 so that we include the actual stop index data
            # add timeframe's splice indexes to splice indexes dict
            splice_indexes[timeframe+'_Start_Index'] = timeframe_splice_start_index
            splice_indexes[timeframe+'_Stop_Index'] = timeframe_splice_stop_index
    # trim all arrays to match entry timeframe's timestamp timeline
    x_column_list = list(x_dict.keys())
    for key in x_column_list:
        # get current key's timeframe
        current_key_timeframe = key.split('_')[0]
        # if current key timeframe is not the entry timeframe
        if current_key_timeframe != entry_timeframe:
            # get timeframe's splice indexes
            timeframe_splice_start_index = splice_indexes[current_key_timeframe+'_Start_Index']
            timeframe_splice_stop_index = splice_indexes[current_key_timeframe+'_Stop_Index']
            # trim current key's data
            x_dict[key] = np.array(x_dict[key])[timeframe_splice_start_index:timeframe_splice_stop_index]
    # for key in x_column_list:
    #     print(key, ': length =', len(x_dict[key]))
    # quit()
    # *************************************************************************************************************************************

    # build pandas dataframe using x_dict *************************************************************************************************
    x_features_dataframe = pd.DataFrame(x_dict)
    print('\n\nX Features Dataset:\n', x_features_dataframe.head(), '\n\n')
    # *************************************************************************************************************************************

    # return x_features_dataframe, and x_column_list
    return x_features_dataframe, x_column_list