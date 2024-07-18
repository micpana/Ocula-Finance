from pandas import read_csv
import numpy as np
import random
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

# ensure reproducibility ******************************************************************************************************
seed = 42
random.seed(seed) # Python's built in random number generator
np.random.seed(seed) # NumPy's random number generator
# *****************************************************************************************************************************

# get data ********************************************************************************************************************
symbol = 'Boom 1000 Index'
timeframe = 'H1'
folder = 'datasets/'
columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']
ohlc_df_path = folder + symbol + timeframe + ".csv"
ohlc_df = read_csv(ohlc_df_path, names=columns, encoding='utf-16')
del ohlc_df['col1']
del ohlc_df['col2']
print('OHLC DF:\n', ohlc_df.head(), '\n\n')
# ohlc_df = ohlc_df.tail(50)
# *****************************************************************************************************************************

# get price and date numpy arrays *********************************************************************************************
dates = np.array(ohlc_df['time'].values, dtype=str) # get numpy array of dates
opens = ohlc_df['open'].values # get numpy array of opening prices
highs = ohlc_df['high'].values # get numpy array of high prices
lows = ohlc_df['low'].values # get numpy array of low prices
closes = ohlc_df['close'].values # get numpy array of closing prices
bodies = closes - opens # get numpy array of candlestick body sizes
candlestick_types = np.where(bodies > 0, 'bullish', 'bearish') # get numpy array of candlestick types
upper_wicks = np.where(bodies > 0, highs - closes, highs - opens) # get numpy array of upper wick sizes
lower_wicks = np.where(bodies > 0, opens - lows, closes - lows) # get numpy array of lower wick sizes
# For better understanding, we can print the arrays
# print("Dates:", dates)
# print('Opening Prices:', opens)
# print('High Prices:', highs)
# print('Low Prices:', lows)
# print('Closing Prices:', closes)
# print('Candlestick Bodies:', bodies)
# print("Candlestick Types:", candlestick_types)
# print("Upper Wicks:", upper_wicks)
# print("Lower Wicks:", lower_wicks)
# *****************************************************************************************************************************

# price spike parameters ******************************************************************************************************
minimum_spike_target_percentage = 1.00 # float
spike_candles_limit = 300 # integer value > 1 or None (to search all forward items)
max_reversal_point_percentage = 0.3 # float
# *****************************************************************************************************************************

# function for finding spikes *************************************************************************************************
def find_spikes(opens_, highs_, lows_, closes_, spike_direction_, show_progress_): # spike direction is up / down
    number_of_items = len(closes_)
    spike_starts_ = np.full(number_of_items, False, dtype=bool) # initialize an array to store whether the candlestick is a spike / spike starting point according to our spike parameters
    for i, (open_price, high_price, low_price, close_price) in tqdm(enumerate(zip(opens_, highs_, lows_, closes_)), desc="Finding Spikes", unit="row", disable= not show_progress_):
        # calculate maximum reversal price
        if spike_direction_ == 'up': maximum_reversal_price = close_price - ((max_reversal_point_percentage / 100) * close_price)
        if spike_direction_ == 'down': maximum_reversal_price = close_price + ((max_reversal_point_percentage / 100) * close_price)

        # calculate spike target price
        if spike_direction_ == 'up': spike_price_target = close_price + ((minimum_spike_target_percentage / 100) * close_price)
        if spike_direction_ == 'down': spike_price_target = close_price - ((minimum_spike_target_percentage / 100) * close_price)

        # determine spike search start and end indexes
        spike_search_start = i+1 # next candle
        spike_search_end = number_of_items if spike_candles_limit == None else spike_search_start + spike_candles_limit # end of list if None, or look at the next n candles only

        # look for spike termination according to our spike parameters, starting from the candle after current candle going forward
        for j, (open_price_, high_price_, low_price_, close_price_) in enumerate(zip(opens_[spike_search_start:spike_search_end], highs_[spike_search_start:spike_search_end], lows_[spike_search_start:spike_search_end], closes_[spike_search_start:spike_search_end])):
            # if maximum reversal point has been hit, break forward loop
            if spike_direction_ == 'up' and low_price_ <= maximum_reversal_price: break # when checking for upward spikes
            if spike_direction_ == 'down' and high_price_ >= maximum_reversal_price: break # when checking for downward spikes

            # if spike price target has been hit, mark as spike start in spike_starts array, and break forward loop
            if high_price_ >= spike_price_target and spike_direction_ == 'up': spike_starts_[i] = True; break # for upward spikes 
            if low_price_ <= spike_price_target and spike_direction_ == 'down': spike_starts_[i] = True; break # for downward spikes

    # calculate the probability (as a percentage) of spikes occuring
    probability_of_spikes_occuring_non_percentage_ = np.mean(spike_starts_)
    probability_of_spikes_not_occuring_non_percentage_ = 1 - probability_of_spikes_occuring_non_percentage_
    probability_of_spikes_occuring_ = probability_of_spikes_occuring_non_percentage_ * 100
    print(probability_of_spikes_occuring_non_percentage_, probability_of_spikes_not_occuring_non_percentage_)
    print(minimum_spike_target_percentage, max_reversal_point_percentage)
    print(probability_of_spikes_occuring_non_percentage_*(minimum_spike_target_percentage/100), probability_of_spikes_not_occuring_non_percentage_*(minimum_spike_target_percentage/100))
    quit()

    # calculate the expected value (EV), a metric used to assess the profitability of a trading strategy over the long term ... Expected Value = (Win Probability * Profit per Win) + (Loss Probability * Loss per Loss)
    expected_value_ = (probability_of_spikes_occuring_non_percentage_ * (minimum_spike_target_percentage)) - (probability_of_spikes_not_occuring_non_percentage_ * (max_reversal_point_percentage))

    # return probability of spikes occuring, expected value, and spike_starts_ array
    return probability_of_spikes_occuring_, expected_value_, spike_starts_
# *****************************************************************************************************************************

# calculate the probability of spikes occuring in historical data *************************************************************
print('Calculating the probability of spikes occuring in historical data...')
probability_of_spikes_occuring, expected_value, spike_starts = find_spikes(opens, highs, lows, closes, 'up', True)
print('Probability of a spike occuring according to historical data is:', probability_of_spikes_occuring, '%')
print('Expected Value (EV):', expected_value)
# *****************************************************************************************************************************
quit()
# limit data for plots if neccessary ******************************************************************************************
limit_data_for_plots = False
limit_to_last = 1000
if limit_data_for_plots == True:
    dates = dates[-limit_to_last:]
    opens = opens[-limit_to_last:]
    highs = highs[-limit_to_last:]
    lows = lows[-limit_to_last:]
    closes = closes[-limit_to_last:]
    spike_starts = spike_starts[-limit_to_last:]
# *****************************************************************************************************************************

# visualize on a ohlc chart if neccessary *************************************************************************************
visualize_ohlc_chart = False
if visualize_ohlc_chart == True:
    bar_width = 0.001 # candlestick width
    wick_width = 0.0005 # wick width
    dates = pd.to_datetime(dates, format='%Y.%m.%d %H:%M') # format the dates for plotting
    dates = dates.values
    for i, (date, open_price, high_price, low_price, close_price, spike_start) in tqdm(enumerate(zip(dates, opens, highs, lows, closes, spike_starts)), desc="Plotting Chart", unit="row"):
        # if theres a spike
        if spike_start == True: plt.plot_date(date, close_price, '.', color='blue', xdate=True)
        # plot ohlc data
        color = 'green' if close_price >= open_price else 'red'  # green for bullish candle, and red for bearish candle
        plt.bar(mdates.date2num(date), abs(close_price - open_price), bar_width, bottom=min(open_price, close_price), color=color) # candlestick body
        if close_price >= open_price: plt.bar(mdates.date2num(date), abs(high_price - close_price), wick_width, bottom=close_price, color=color) # upper wick for bullish candle
        else: plt.bar(mdates.date2num(date), abs(high_price - open_price), wick_width, bottom=open_price, color=color) # upper wick for bearish candle
        if close_price >= open_price: plt.bar(mdates.date2num(date), abs(open_price - low_price), wick_width, bottom=low_price, color=color) # lower wick for bullish candle
        else: plt.bar(mdates.date2num(date), abs(close_price - low_price), wick_width, bottom=low_price, color=color) # lower wick for bearish candle
    # show plot
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(symbol + ' Chart')
    plt.xticks(rotation=90)
    # plt.grid(True)
    plt.autoscale()
    plt.show()
# *****************************************************************************************************************************

# simulation parameters *******************************************************************************************************
number_of_simulations = 1000000
candlesticks_to_simulate = 10
use_normal_distribution = True
# *****************************************************************************************************************************

# get means and standard deviations *******************************************************************************************
bodies_mean = bodies.mean()
bodies_standard_deviation = bodies.std()
upper_wicks_mean = upper_wicks.mean()
upper_wicks_standard_deviation = upper_wicks.std()
lower_wicks_mean = lower_wicks.mean()
lower_wicks_standard_deviation = lower_wicks.std()
# *****************************************************************************************************************************

# function for running simulation using normal distribution *******************************************************************
if use_normal_distribution == True:
    def simulate(opens_, highs_, lows_, closes_):
        simulated_ohlc_ = np.zeros((number_of_simulations, candlesticks_to_simulate, 4)) # initialize array to store all simulated ohlc data
        last__historical_close = closes_[-1] # variable to store the value of the last close in historical data
        simulated_bodies = np.random.normal(loc=bodies_mean, scale=bodies_standard_deviation, size=number_of_simulations*candlesticks_to_simulate) # simulated candlestick bodies
        simulated_upper_wicks = np.random.normal(loc=upper_wicks_mean, scale=upper_wicks_standard_deviation, size=number_of_simulations*candlesticks_to_simulate) # simulated candlestick upper wicks
        simulated_lower_wicks = np.random.normal(loc=lower_wicks_mean, scale=lower_wicks_standard_deviation, size=number_of_simulations*candlesticks_to_simulate) # simulated candlestick lower wicks
        for i in tqdm(range(number_of_simulations), desc="Simulating", unit="row"):
            # generate current simulation's data
            for j in range(candlesticks_to_simulate):
                last_close = last__historical_close if j == 0 else simulated_ohlc_[i][j-1][3] # if on current simulation's first candlestick, use last close in historical data, else use the last simulated closing price
                # simulate data
                open_price = last_close
                close_price = open_price + simulated_bodies[i+j]
                high_price = close_price + simulated_upper_wicks[i+j] if close_price >= open_price else open_price + simulated_upper_wicks[i+j]
                low_price = open_price - simulated_lower_wicks[[i+j]] if close_price >= open_price else close_price - simulated_lower_wicks[i+j]
                # set last_close as close_price
                last_close = close_price
                # add simulated values to their respective arrays
                simulated_ohlc_[i][j][0] = open_price
                simulated_ohlc_[i][j][1] = high_price
                simulated_ohlc_[i][j][2] = low_price
                simulated_ohlc_[i][j][3] = close_price
        # return simulated ohlc data
        return simulated_ohlc_
# *****************************************************************************************************************************

# function for running simulation without assuming any distribution ***********************************************************
if use_normal_distribution == False:
    def simulate(opens_, highs_, lows_, closes_):
        simulated_ohlc_ = np.zeros((number_of_simulations, candlesticks_to_simulate, 4)) # initialize array to store all simulated ohlc data
        last__historical_close = closes_[-1] # variable to store the value of the last close in historical data
        for i in tqdm(range(number_of_simulations), desc="Simulating", unit="row"):
            # generate current simulation's data
            for j in range(candlesticks_to_simulate):
                last_close = last__historical_close if j == 0 else simulated_ohlc_[i][j-1][3] # if on current simulation's first candlestick, use last close in historical data, else use the last simulated closing price
                random_index = np.random.choice(len(closes_)) # randomly select an index in historical ohlc data
                # randomly selected candlestick's data
                selected_open = opens_[random_index]; selected_high = highs_[random_index]; selected_low = lows_[random_index]; selected_close = closes_[random_index]
                # simulate data
                open_price = last_close
                high_price = open_price + (selected_high - selected_open)
                low_price = open_price - (selected_open - selected_low)
                close_price = open_price + (selected_close - selected_open)
                # set last_close as close_price
                last_close = close_price
                # add simulated values to their respective arrays
                simulated_ohlc_[i][j][0] = open_price
                simulated_ohlc_[i][j][1] = high_price
                simulated_ohlc_[i][j][2] = low_price
                simulated_ohlc_[i][j][3] = close_price
        # return simulated ohlc data
        return simulated_ohlc_
# *****************************************************************************************************************************

# run simulation and get simulated ohlc data **********************************************************************************
simulated_ohlc = simulate(opens, highs, lows, closes) # 3d array, shape=(rows, embedded rows, columns)
print('Simulated OHLC:', simulated_ohlc)
most_recent_close = closes[-1]
highest_simulated_value = np.max(simulated_ohlc[:, :, 1])
lowest_simulated_value = np.min(simulated_ohlc[:, :, 2])
highest_simulated_percentage_change = (highest_simulated_value / most_recent_close) * 100
lowest_simulated_percentage_change = (lowest_simulated_value / most_recent_close) * 100
print('Most recent close:', most_recent_close)
print('Highest simulated value:', highest_simulated_value)
print('Lowest simulated value:', lowest_simulated_value)
print('Highest simulated value`s percentage change from most recent close:', highest_simulated_percentage_change, '%')
print('Lowest simulated value`s percentage change from most recent close:', lowest_simulated_percentage_change, '%')
# *****************************************************************************************************************************

# get most likey path from the simulation *************************************************************************************
most_likely_path = np.mean(simulated_ohlc, axis=0) # get the mean OHLC values across all simulations at each time step
# extract separate arrays for mean opens, highs, lows, and closes
mean_opens = most_likely_path[:, 0]
mean_highs = most_likely_path[:, 1]
mean_lows = most_likely_path[:, 2]
mean_closes = most_likely_path[:, 3]
most_likely_highest_value = np.max(mean_highs)
most_likey_lowest_value = np.min(mean_lows)
most_likely_highest_percentage_change = (most_likely_highest_value / most_recent_close) * 100
most_likely_lowest_percentage_change = (most_likey_lowest_value / most_recent_close) * 100
print('Most Likey highest value:', most_likely_highest_value)
print('Most likey lowest value:', most_likey_lowest_value)
print('Most likey highest value`s percentage change from most recent close:', most_likely_highest_percentage_change, '%')
print('Most likey lowest value`s percentage change from most recent close:', most_likely_lowest_percentage_change, '%')
# *****************************************************************************************************************************
quit()
# calculate the probability of the next candlestick being a spike start according to our simulated data and spike parameters **
print('Calculating the probability of the next candle being a spike start...')
spike_starts = np.full(number_of_simulations, False, dtype=bool) # initialize an array to store whether the candlestick is a spike / spike starting point according to our spike parameters
for i in tqdm(range(number_of_simulations), desc="Calculating", unit="row"):
    simulation = simulated_ohlc[i] # contains embedded rows (candlestick simulations), columns
    # get arrays for simulated opens, highs, lows, closes
    simulated_opens = simulation[:, 0]
    simulated_highs = simulation[:, 1]
    simulated_lows = simulation[:, 2]
    simulated_closes = simulation[:, 3]
    # check if candlestick is a spike start
    probability_of_spikes_occuring_, break_even_risk_to_reward_, spike_starts_ = find_spikes(simulated_opens, simulated_highs, simulated_lows, simulated_closes, 'up', False)
    # store the first simulated candlestick's spike start status as the current simulation's spike start status
    spike_starts[i] = spike_starts_[0]

# calculate the probability (as a percentage) of spikes occuring
probability_of_spikes_occuring = np.mean(spike_starts) * 100
# calculate the break even risk-to-reward ratio ... (probability of spikes not occuring / probability of spikes occuring)
break_even_risk_to_reward = (100 - probability_of_spikes_occuring) / probability_of_spikes_occuring
print('Probability of the next candle being a spike according to simulations done is:', probability_of_spikes_occuring, '%')
print('Break even Risk-to-Reward: 1:', break_even_risk_to_reward)
# *****************************************************************************************************************************