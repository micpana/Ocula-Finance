from pandas import read_csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
from tqdm import tqdm
from collections import deque
import collections
from sklearn.ensemble import RandomForestClassifier
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

#state seed
seed = 422

# get data ********************************************************************************************************************
symbol = 'EURUSD'
timeframe = 'M15'
folder = 'datasets/'
columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']
ohlc_df_path = folder + symbol + timeframe + ".csv"
ohlc_df = read_csv(ohlc_df_path, names=columns, encoding='utf-16')
del ohlc_df['col1']
del ohlc_df['col2']
print('OHLC DF:\n', ohlc_df.head(), '\n\n')
# *****************************************************************************************************************************

# limit dataset for faster testing purposes
# ohlc_df = ohlc_df.tail(10000)

# lookback
lookback = 300

# takeprofit percentage
takeprofit_percentage = 0.11

# stoploss percentage
stoploss_percentage = 0.5

# feature engineering *********************************************************************************************************
# get numpy array of dates
dates = np.array(ohlc_df['time'].values, dtype=str)
# get numpy array of opening prices
opens = ohlc_df['open'].values
# get numpy array of high prices
highs = ohlc_df['high'].values
# get numpy array of low prices
lows = ohlc_df['low'].values
# get numpy array of closing prices
closes = ohlc_df['close'].values

# calculate stoploss and takeprofit prices for buy conditions
buy_takeprofit_prices = closes + ((takeprofit_percentage / 100) * closes)
buy_stoploss_prices = closes - ((stoploss_percentage / 100) * closes)

# calculate stoploss and takeprofit prices for sell conditions
sell_takeprofit_prices = closes - ((takeprofit_percentage / 100) * closes)
sell_stoploss_prices = closes + ((stoploss_percentage / 100) * closes)

# initialize df dict
df_dict = {}
x_column_name_first_section = 'Close_'
for i in range(lookback):
    column_name = x_column_name_first_section + str(i+1)
    df_dict[column_name] = deque([])

# list of x df columns
x_column_list = list(df_dict.keys())

# initialize y columns
y_column_name = 'Action'
df_dict[y_column_name] = deque([])

# initialize ohlc arrays matching engineered features, and the dates as well 
dates_match = deque([])
opens_match = deque([])
highs_match = deque([])
lows_match = deque([])
closes_match = deque([])

# determine start and stop indexes in main ohlc df for feature engineering
main_loop_start_index = 0
main_loop_end_index = len(closes)-lookback-1

# populate df dict
for i in tqdm(range(main_loop_start_index, main_loop_end_index, +1), desc="Feature Engineering Stage 1", unit="row"):
    # generate current row data by lookback 
    for j in range(lookback):
        # current column name
        current_column_name = x_column_name_first_section + str(j+1)
        # current closing price
        current_closing_price = closes[i+j]
        # add closes value to df dict
        df_dict[current_column_name].append(current_closing_price)
        # last lookback candle index 
        reference_candle_index = i+j

    # current take profits and stoplosses
    buy_takeprofit_price = buy_takeprofit_prices[reference_candle_index]
    buy_stoploss_price = buy_stoploss_prices[reference_candle_index]
    sell_takeprofit_price = sell_takeprofit_prices[reference_candle_index]
    sell_stoploss_price = sell_stoploss_prices[reference_candle_index]

    # current ohlc data + date
    current_date = dates[reference_candle_index]
    current_open = opens[reference_candle_index]
    current_high = highs[reference_candle_index]
    current_low = lows[reference_candle_index]
    current_close = closes[reference_candle_index]

    # generate y data
    action = 'Do Nothing'
    # check of a buy
    for k in range(reference_candle_index, len(closes), +1):
        # get current bar's high and low prices
        current_forward_high_price = highs[k]; current_forward_low_price = lows[k]
        # if buy takeprofit has been hit, set action to Buy and break loop
        if current_forward_high_price >= buy_takeprofit_price: action = 'Buy'; break
        # if buy stoploss has been hit, set action to Do Nothing and break loop
        if current_forward_low_price <= current_close: action = 'Do Nothing'; break

    # only check for a sell if no buy was found
    if action != 'Buy':
        # check for a sell 
        for k in range(reference_candle_index, len(closes), +1):
            # get current bar's high and low prices
            current_forward_high_price = highs[k]; current_forward_low_price = lows[k]
            # if sell takeprofit has been hit, set action to Sell and break loop
            if current_forward_low_price <= sell_takeprofit_price: action = 'Sell'; break
            # if sell stoploss has been hit, 
            if current_forward_high_price >= current_close: action = 'Do Nothing'; break

    # add action to df dict
    df_dict[y_column_name].append(action)

    # add data to ohlc arrays matching engineered features
    dates_match.append(current_date) # date matching looback'th candle
    opens_match.append(current_open) # open matching looback'th candle
    highs_match.append(current_high) # high matching looback'th candle
    lows_match.append(current_low) # low matching looback'th candle
    closes_match.append(current_close) # close matching looback'th candle

# create dataframe / main dataset
dataframe = pd.DataFrame(df_dict)
print('Dataset:\n', dataframe.head(), '\n\n')
print('Actions:\n', dataframe[y_column_name].value_counts(), '\n\n')

# separate dataset into x and y dataset
x_dataframe = dataframe.filter(x_column_list)
y_dataframe = dataframe.filter([y_column_name])

# create x and y numpy arrays
x = x_dataframe.values
y = y_dataframe.values

# perceive single row feature difference in x
print('Feature Engineering Stage 2...')
x_base_grid, random_grid = np.meshgrid(x[:, 0], np.random.rand(x.shape[1]), indexing='ij') # create x meshgrid
x_feature_differences = ((x - x_base_grid) / x_base_grid) * 100

# set x feature differences as x
x = x_feature_differences
# *****************************************************************************************************************************

# split data into x_train, x_test, y_train, and y_test. don't shuffle *********************************************************
# test set size
test_size = 0.2

# calculate split indices
split_indices = int((1-test_size) * len(x))

# create a test set that will be unseen from the model, either directly or via splits
x_test = x[split_indices:]
y_test = y[split_indices:]

# get x and y without data used for the test set
x_train = x[:split_indices]
y_train = y[:split_indices]

# perform a train validation split using training data
validation_size = 0.2
x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train, test_size=validation_size, shuffle=True, random_state=seed)
# *****************************************************************************************************************************

# turn deque lists with match data into numpy arrays **************************************************************************
dates_match = np.array(dates_match)
opens_match = np.array(opens_match)
highs_match = np.array(highs_match)
lows_match = np.array(lows_match)
closes_match = np.array(closes_match)
# *****************************************************************************************************************************

# get test ohlc arrays, and the dates as well *********************************************************************************
test_dates = dates_match[split_indices:]
test_opens = opens_match[split_indices:]
test_highs = highs_match[split_indices:]
test_lows = lows_match[split_indices:]
test_closes = closes_match[split_indices:]
# *****************************************************************************************************************************

"""
    On class imbalances:
    - SMOTE turned out better than training the data just as it is
    - BalancedRandomForestClassifier turned out better than using SMOTE
"""
# balance classes using SMOTE *************************************************************************************************
balance_classes = True
if balance_classes == True:
    # print shape of x train and y train before SMOTE
    print('Shape of x_train before smote:', x_train.shape)
    print('Shape of y_train before smote:', y_train.shape, '\n\n')

    # get class counts before smote
    print('Class counts before SMOTE:', collections.Counter(np.ravel(y_train)), '\n\n')

    # import SMOTE and perform SMOTE operations
    smote = SMOTE()
    x_train, y_train = smote.fit_resample(x_train, y_train)

    # print shape of x train and y train after smote
    print('Shape of x_train after smote:', x_train.shape)
    print('Shape of y_train after smote:', y_train.shape, '\n\n')

    # get class counts after smote
    print('Class counts after SMOTE:', collections.Counter(y_train), '\n\n')
# *****************************************************************************************************************************

# train model and get y pred **************************************************************************************************
# creating a RF classifier model
model = RandomForestClassifier(n_estimators = 100, verbose=2, n_jobs=-1, random_state=seed)  

# train model
model.fit(x_train, y_train)
 
# performing predictions on the test dataset
y_pred = model.predict(x_test)

# # seeker
# from seeker import Seeker

# # initialize Seeker
# seeker = Seeker()

# # Seeker parameters
# seeker.verbosity = True
# seeker.regression = False

# # run test
# performance_results = seeker.test(x_train, np.array(y_train, dtype=str), x_test, np.array(y_test, dtype=str))

# # seek results
# y_pred = performance_results['seek_results']
# *****************************************************************************************************************************

# print out model perfomance **************************************************************************************************
# using metrics module for accuracy calculation
print('\n\nACCURACY OF THE MODEL:', accuracy_score(y_test, y_pred), '\n\n')

# print classification report for model
print('CLASSIFICATION REPORT:\n', classification_report(y_test, y_pred), '\n\n')

# print confusion matrix
confusion_matrix_ = pd.DataFrame(
    confusion_matrix(y_test, y_pred, labels=['Buy', 'Do Nothing', 'Sell']), 
    index=['Buy (Actual)', 'Do Nothing (Actual)', 'Sell (Actual)'], 
    columns=['Buy (Predicted)', 'Do Nothing (Predicted)', 'Sell (Predicted)']
)
print('CONFUSION MATRIX:\n', confusion_matrix_, '\n\n')

# print validation confusion matrix
print('***VALIDATION:')
y_pred_val = model.predict(x_validation)
confusion_matrix = pd.DataFrame(
    confusion_matrix(y_validation, y_pred_val, labels=['Buy', 'Do Nothing', 'Sell']), 
    index=['Buy (Actual)', 'Do Nothing (Actual)', 'Sell (Actual)'], 
    columns=['Buy (Predicted)', 'Do Nothing (Predicted)', 'Sell (Predicted)']
)
print('CONFUSION MATRIX:\n', confusion_matrix, '\n\n')
# *****************************************************************************************************************************

# visualize actual vs predicted ***********************************************************************************************
# format the dates for plotting
test_dates_datetime = pd.to_datetime(test_dates, format='%Y.%m.%d %H:%M')

# replace all Buys with 1
y_test[y_test == 'Buy'] = 1
y_pred[y_pred == 'Buy'] = 1

# replace all Do Nothings with 0
y_test[y_test == 'Do Nothing'] = 0
y_pred[y_pred == 'Do Nothing'] = 0

# replace all Sells with -1
y_test[y_test == 'Sell'] = -1
y_pred[y_pred == 'Sell'] = -1

# plot comparisons
plt.plot_date(test_dates_datetime, y_test, label='Actual', fmt='-', xdate=True)
plt.plot_date(test_dates_datetime, y_pred, label='Predicted', fmt='-', xdate=True)
plt.xticks(rotation=90)
plt.title('Predicted vs Actual')
plt.grid(True)
plt.legend()
plt.show()
# *****************************************************************************************************************************

# visualize y test data (actual / predicted) on candlestick chart *************************************************************
# plot y_pred on chart
for i, (date, close, y_pred) in tqdm(enumerate(zip(test_dates_datetime, test_closes, y_test)), desc="Plotting Signals", unit="row"):
    # buys
    if y_pred == 1:
        plt.plot_date(date, close, '.', color='blue', xdate=True)

    # do nothing
    if y_pred == 0:
        plt.plot_date(date, close, '.', color='black', xdate=True)

    # sells
    if y_pred == -1:
        plt.plot_date(date, close, '.', color='orange', xdate=True)

# parameters for plot rectangles / bars, for the candle bodies and wicks
bar_width = 0.01 
wick_width = 0.0005

# # plot candlesticks
for i, (date, open_price, high_price, low_price, close_price) in enumerate(zip(test_dates_datetime.values, test_opens, test_highs, test_lows, test_closes)):
    color = 'green' if close_price >= open_price else 'red'  # green for bullish candle, and red for bearish candle
    # candlestick body
    plt.bar(mdates.date2num(date), abs(close_price - open_price), bar_width, bottom=min(open_price, close_price), color=color)
    # upper wick
    if close_price >= open_price: plt.bar(mdates.date2num(date), abs(high_price - close_price), wick_width, bottom=close_price, color=color) # bullish candle
    else: plt.bar(mdates.date2num(date), abs(high_price - open_price), wick_width, bottom=open_price, color=color) # bearish candle
    # lower wick
    if close_price >= open_price: plt.bar(mdates.date2num(date), abs(open_price - low_price), wick_width, bottom=low_price, color=color) # bullish candle
    else: plt.bar(mdates.date2num(date), abs(close_price - low_price), wick_width, bottom=low_price, color=color) # bearish candle

# show plot
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(symbol + ' Chart')
plt.xticks(rotation=90)
# plt.grid(True)
plt.autoscale()
plt.show()
# *****************************************************************************************************************************