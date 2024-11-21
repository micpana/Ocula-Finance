import numpy as np
from collections import deque
from tqdm import tqdm
from data_acquisition import acquire_data
from symbol_config import get_symbol_list, get_symbol_config

# percentile value to investigate *********************************************************************************************************
percentile_value_to_investigate = 79.71129206201581 # to be selected from the percentile of the best performing symbol's set target and forecast period, as per desired/chosen performance metrics
# *****************************************************************************************************************************************

# get list of symbols *********************************************************************************************************************
list_of_symbols = get_symbol_list()
list_of_symbols = ['USDJPY'] # override ... comment it out when not in use
# printout the list of symbols being used
print('\n\nRunning target statistics for the following symbols:', list_of_symbols)
# *****************************************************************************************************************************************

# state entry timeframe ... choose between Monthly, Weekly, Daily, H4, H1, M30, M15, M5, and M1 *******************************************
entry_timeframe = 'M15'
# *****************************************************************************************************************************************

# timeframes array ... only use the entry timeframe ***************************************************************************************
timeframes = [entry_timeframe]
# *****************************************************************************************************************************************

# call module ... use 'training' to get more data *****************************************************************************************
call_module = 'training'
# *****************************************************************************************************************************************

# loop through symbols ********************************************************************************************************************
for symbol in list_of_symbols:
    # signal the start of the symbol's target statistics retrieval
    print('\n\nRunning Target Statistics for', symbol, '******************************','\n\n')

    # get symbol data ***********************************************************************************************************
    # get symbol config
    symbol_config = get_symbol_config(symbol)

    # reward ... minimum buy or sell target percentage
    reward = symbol_config['target']
                
    # forecast period
    forecast_period = symbol_config['forecast_period']
    forecast_period = 8 # override ... comment it out when not in use
    # ***************************************************************************************************************************

    # get symbol's ohlc data dict with every stated timeframe's ohlc df *********************************************************
    ohlc_data_dict = acquire_data(symbol, timeframes, call_module, None, None)
    # ***************************************************************************************************************************

    # get numpy arrays for dates, opens, highs, lows, and closes ****************************************************************
    dates = ohlc_data_dict[entry_timeframe]['time'].values
    opens = ohlc_data_dict[entry_timeframe]['open'].values
    highs = ohlc_data_dict[entry_timeframe]['high'].values
    lows = ohlc_data_dict[entry_timeframe]['low'].values
    closes = ohlc_data_dict[entry_timeframe]['close'].values
    # ***************************************************************************************************************************

    # initialize deque array to store all found target values as absolute values (since its for both market directions) *********
    absolute_target_values = deque([])
    # ***************************************************************************************************************************

    # generate target statistics ************************************************************************************************
    for i in tqdm(range(len(closes)), desc="Target Statistics Generation", unit="row"):
        # current closing price
        current_closing_price = closes[i]

        # next forecast period highs
        next_forecast_period_highs = highs[i:i+forecast_period+1]
        # next forecast period lows
        next_forecast_period_lows = lows[i:i+forecast_period+1]

        # highest price in the next forecast period
        highest_price_in_the_next_forecast_period = np.max(next_forecast_period_highs)
        # lowest price in the next forecast period
        lowest_price_in_the_next_forecast_period = np.min(next_forecast_period_lows)

        # highest percentage change in the next forecast period
        highest_percentage_change_in_the_next_forecast_period = ((highest_price_in_the_next_forecast_period - current_closing_price) / current_closing_price) * 100 # ((b - a) / a) * 100
        # lowest percentage change in the next forecast period
        lowest_percentage_change_in_the_next_forecast_period = ((lowest_price_in_the_next_forecast_period - current_closing_price) / current_closing_price) * 100 # ((b - a) / a) * 100

        # add absolute value of highest_percentage_change_in_the_next_forecast_period to absolute_target_values
        absolute_target_values.append(abs(highest_percentage_change_in_the_next_forecast_period))
        # add absolute value of lowest_percentage_change_in_the_next_forecast_period to absolute_target_values
        absolute_target_values.append(abs(lowest_percentage_change_in_the_next_forecast_period))
    # ***************************************************************************************************************************

    # convert absolute_target_values into a numpy array *************************************************************************
    absolute_target_values = np.array(absolute_target_values)
    # ***************************************************************************************************************************

    # statistics ****************************************************************************************************************
    # percentages to use for percentiles
    percentages_for_percentiles = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    # percentiles
    percentiles = np.percentile(absolute_target_values, percentages_for_percentiles)
    # print percentiles marked by their percentage
    print('\n\n', symbol, 'Percentiles:')
    for percentage, value in zip(percentages_for_percentiles, percentiles):
        print(percentage, 'th percentile:', value)
    # percentile for symbol's set target
    percentile = np.mean(np.array(absolute_target_values) <= reward) * 100
    print('\n\n', symbol, 'target (', reward,') in', percentile, 'th percentile')
    # value on symbol data's nth percentile
    value = np.percentile(absolute_target_values, percentile_value_to_investigate)
    print(symbol, 'ideal target to investigate:', value)
    # ***************************************************************************************************************************
# *****************************************************************************************************************************************
