from pandas import read_csv
import numpy as np
import random
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
from collections import deque

# get data ********************************************************************************************************************
symbol = 'Boom 1000 Index'
timeframe = 'M1'
folder = 'datasets/'
columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']
ohlc_df_path = folder + symbol + timeframe + ".csv"
ohlc_df = read_csv(ohlc_df_path, names=columns, encoding='utf-16')
del ohlc_df['col1']
del ohlc_df['col2']
print('OHLC DF:\n', ohlc_df.head(), '\n\n')
ohlc_df = ohlc_df.head(10000)
# *****************************************************************************************************************************

# get price and date numpy arrays *********************************************************************************************
dates = np.array(ohlc_df['time'].values, dtype=str) # get numpy array of dates
opens = ohlc_df['open'].values # get numpy array of opening prices
highs = ohlc_df['high'].values # get numpy array of high prices
lows = ohlc_df['low'].values # get numpy array of low prices
closes = ohlc_df['close'].values # get numpy array of closing prices
# *****************************************************************************************************************************

# initialize arrays to store last structure lows and last structure highs *****************************************************
last_structure_lows = deque([])
last_structure_highs = deque([])
# *****************************************************************************************************************************

# fill up last structure lows and last structure highs arrays *****************************************************************
for i in tqdm(range(len(closes)), desc="Extracting Turning Points", unit="row"):
    # loop back to find low
    for j in range(i, -1, -1):
        most_recent_candle_low = lows[j]
        second_most_recent_candle_low = lows[j-1]
        third_most_recent_candle_low = lows[j-2]

        # if j is less than index 2 (3 items), it means we no longer have sufficient candles for a structure low, therefore pick the lowest low available as the structure low
        if j < 2: 
            last_structure_lows.append(np.min(lows[0:2])) # smallest of the first 2 candle lows
            break
        else:
            # look for a structure low match
            if second_most_recent_candle_low <= most_recent_candle_low and second_most_recent_candle_low <= third_most_recent_candle_low:
                last_structure_lows.append(second_most_recent_candle_low) # structure low
                break

    # loop back to find high
    for j in range(i, -1, -1):
        most_recent_candle_high = highs[j]
        second_most_recent_candle_high = highs[j-1]
        third_most_recent_candle_high = highs[j-2]

        # if j is less than index 2 (3 items), it means we no longer have sufficient candles for a structure high, therefore pick the highest high available as the structure high
        if j < 2: 
            last_structure_highs.append(np.max(highs[0:2])) # highest of the first 2 candle highs
            break
        else:
            # look for a structure high match
            if second_most_recent_candle_high >= most_recent_candle_high and second_most_recent_candle_high >= third_most_recent_candle_high:
                last_structure_highs.append(second_most_recent_candle_high) # structure high
                break
# *****************************************************************************************************************************

# state period for calculating averages and the averages type *****************************************************************
period = 100
averages_type = 'SMA' # SMA / EMA
as_is = False
# *****************************************************************************************************************************

# SMA and EMA functions *******************************************************************************************************
def simple_moving_average(prices, window_size):
    weights = np.ones(window_size) / window_size
    sma = np.convolve(prices, weights, mode='valid')
    return sma

def exponential_moving_average(prices, window_size):
    ema = np.zeros_like(prices)
    alpha = 2 / (window_size + 1)
    ema[0] = prices[0]
    for i in range(1, len(prices)):
        ema[i] = alpha * prices[i] + (1 - alpha) * ema[i - 1]
    return ema
# *****************************************************************************************************************************

# convert structure arrays from deque to numpy arrays *************************************************************************
last_structure_highs = np.array(last_structure_highs)
last_structure_lows = np.array(last_structure_lows)
# *****************************************************************************************************************************

# function to make consecutive structures unique ******************************************************************************
def make_consecutive_unique(arr):
    result = deque([])
    prev = None
    for num in arr:
        if num != prev:
            result.append(num)
        prev = num
    result = np.array(result)
    return result
# *****************************************************************************************************************************

# function to calculate averages as is ****************************************************************************************
def averages_as_is(last_structure_points, window_size):
    averages = deque([])
    # loop through structure points
    for i in range(window_size, len(last_structure_points), +1):
        # unique structure points from index 0 up until current index
        unique_structure_points = make_consecutive_unique(last_structure_points[0:i+1]) # i + 1 coz we actually want the current structure point included
        # get structure points to average (last 'windows size' items) in unique_structure_points
        if len(unique_structure_points) < window_size:
            structure_points_to_average = unique_structure_points
        else:
            structure_points_to_average = unique_structure_points[-window_size:]
        # get average
        average = np.sum(structure_points_to_average) / len(structure_points_to_average)
        # append average to averages
        averages.append(average)
    # turn deque array to numpy array
    averages = np.array(averages)
    # return averages
    return averages
# *****************************************************************************************************************************

# get structure averages ******************************************************************************************************
if as_is == False:
    if averages_type == 'SMA':
        structure_high_averages = simple_moving_average(last_structure_highs, period)
        structure_low_averages = simple_moving_average(last_structure_lows, period)
    elif averages_type == 'EMA':
        structure_high_averages = exponential_moving_average(last_structure_highs, period)
        structure_low_averages = exponential_moving_average(last_structure_lows, period)
    else:
        print('Invalid averages type:', averages_type)
        quit()
else:
    structure_high_averages = averages_as_is(last_structure_highs, period)
    structure_low_averages = averages_as_is(last_structure_lows, period)
# *****************************************************************************************************************************

# get closing prices SMA ******************************************************************************************************
closing_prices_averages = simple_moving_average(closes, period)
# *****************************************************************************************************************************

# make sure the rest of the arrays match the length of the averages (which is now length of other arrays - averages period) ***
length_of_averages = len(structure_high_averages)
dates = dates[-length_of_averages:]
opens = opens[-length_of_averages:]
highs = highs[-length_of_averages:]
lows = lows[-length_of_averages:]
closes = closes[-length_of_averages:]
last_structure_highs = last_structure_highs[-length_of_averages:]
last_structure_lows = last_structure_lows[-length_of_averages:]
# *****************************************************************************************************************************

# plot chart ******************************************************************************************************************
# convert dates to matplotlib date format
dates = [mdates.datestr2num(date) for date in dates]

# combine data into OHLC format
ohlc = np.array([[dates[i], opens[i], highs[i], lows[i], closes[i]] for i in range(len(dates))])

# plotting
fig, ax = plt.subplots(figsize=(10, 6))

# plot OHLC data
candlestick_ohlc(ax, ohlc, width=0.0003, colorup='green', colordown='red')

# plot market structure points as dots (scatter)
ax.scatter(dates, last_structure_highs, label='Last Structure Highs', color='green', marker='o', s=1)
ax.scatter(dates, last_structure_lows, label='Last Structure Lows', color='red', marker='o', s=1)

# plot structure averages
ax.plot(dates, structure_high_averages, label='Structure Highs', color='blue')
ax.plot(dates, structure_low_averages, label='Structure Lows', color='orange')

# plot closes SMA
ax.plot(dates, closing_prices_averages, label='Closes SMA', color='purple')

# formatting the x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d %H:%M'))
# ax.xaxis.set_major_locator(mdates.DayLocator()) # here the max number of ticks is 1000
ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=len(dates))) # set a custom locator to customize the number of ticks

# set x-axis limits to ensure proper spacing
ax.set_xlim(dates[0] - 0.5, dates[-1] + 0.5)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title(symbol + ' Chart')
plt.legend(loc="upper right")
# plt.grid()
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()
# *****************************************************************************************************************************