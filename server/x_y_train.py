from x_y_feature_engineering import engineer_x_y
from sklearn.preprocessing import MinMaxScaler
import random
import numpy as np
from collections import deque
from tqdm import tqdm
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_sample_weight
from imblearn.over_sampling import SMOTE
import pandas as pd
import collections
from xgboost import XGBClassifier
from xgboost import XGBRegressor
from sklearn.preprocessing import LabelEncoder
from symbol_config import get_symbol_list, get_symbol_config
import matplotlib.dates as mdates
from mplfinance.original_flavor import candlestick_ohlc
import pickle
from cryptography.fernet import Fernet
from settings import get_scaler_path, get_model_path, get_training_log_path, show_plots_during_training, get_model_performance_visual_insights_path
import json
from minutes_to_hours_and_minutes import minutes_to_hours_and_minutes

# ensure reproducibility ******************************************************************************************************************
seed = 42
random.seed(seed) # Python's built in random number generator
np.random.seed(seed) # NumPy's random number generator
# *****************************************************************************************************************************************

# y type ...  buy or sell / minimum maximum
y_type = 'buy or sell'

# smote ***********************************************************************************************************************************
balance_classes = False
# *****************************************************************************************************************************************

# graph settings **************************************************************************************************************************
# actual vs predicted
visualize_actual_vs_predicted = True
# feature importance
visualize_feature_importance = True
# equity graph
visualize_equity_graph = True
# buy sell ohlc graph
visualize_ohlc_buy_sell_graph = True
# *****************************************************************************************************************************************

# get list of symbols *********************************************************************************************************************
list_of_symbols = get_symbol_list()
# printout the list of symbols being used
print('\n\nRunning model training for the following symbols:', list_of_symbols)
# *****************************************************************************************************************************************

# loop through symbols ********************************************************************************************************************
for symbol in list_of_symbols:
    # signal the start of the current symbol's model training
    print('Training', symbol, 'Model...\n\n')

    # get symbol data ***********************************************************************************************************
    # get symbol config
    symbol_config = get_symbol_config(symbol)

    # reward ... minimum buy or sell target percentage
    reward = symbol_config['target']

    # risk target divisor
    risk_target_divisor = symbol_config['risk_target_divisor']

    # risk:reward
    risk_to_reward_ratio = '1:'+str(risk_target_divisor)

    # risk ... stoploss
    risk = reward / risk_target_divisor
    # ***************************************************************************************************************************

    # get feature engineered dataset
    dataset, x_column_list, y_column_list, entry_timeframe, timeframes = engineer_x_y(symbol, y_type, 'training')

    # test size
    test_size = 0.2

    # test dataset length
    test_dataset_length = int(test_size * len(dataset))

    # train dataset length
    train_dataset_length = int(len(dataset) - test_dataset_length)

    # split dataset into train and test
    train_dataset = dataset.head(train_dataset_length)
    test_dataset =  dataset.tail(test_dataset_length)

    # get entry timeframe's dates array from the train data
    train_dates = train_dataset[entry_timeframe+'_Timestamp'].values

    # get entry timeframe's dates array from test data
    test_dates = test_dataset[entry_timeframe+'_Timestamp'].values

    # get entry timeframe's open, high, low, and closing prices arrays from test data
    test_opens = test_dataset[entry_timeframe+'_Open'].values
    test_highs = test_dataset[entry_timeframe+'_High'].values
    test_lows = test_dataset[entry_timeframe+'_Low'].values
    test_closes = test_dataset[entry_timeframe+'_Close'].values

    # get extra y data (non target variables)
    test_max_percentages_down = test_dataset['Max % Down'].values
    test_max_percentages_up = test_dataset['Max % Up'].values
    test_trade_closing_percentages = test_dataset["Trade's Session Closing %"].values

    # delete every timeframe's timestamp column from every dataset (train & test)
    for timeframe in timeframes:
        del train_dataset[timeframe+'_Timestamp']
        del test_dataset[timeframe+'_Timestamp']
    #     print('*******', timeframe)
    #     # print(train_dataset[timeframe+'_Timestamp'].values.tolist())
    #     print(test_dataset[timeframe+'_Timestamp'].values.tolist()[:100])
    #     print('*******', timeframe, '******')
    # quit()

    # shuffle train dataset
    train_dataset = train_dataset.sample(frac=1.0)

    # get our train and test sets
    x_train = train_dataset.filter(x_column_list).values
    y_train = train_dataset.filter(y_column_list).values
    x_test = test_dataset.filter(x_column_list).values
    y_test = test_dataset.filter(y_column_list).values

    # print(len(y_test))
    # print(len(test_closes))
    # print(y_train)
    # print(y_test)
    # quit()

    # print data shapes
    print('\n\nX Train Shape: ', x_train.shape)
    print('Y Train Shape: ', y_train.shape)
    print('X Test Shape: ', x_test.shape)
    print('Y Test Shape: ', y_test.shape, '\n\n')

    # scale x data
    min_max_scaler = MinMaxScaler()
    scaler = min_max_scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)

    # minimum maximum ***********************************************************************************************************
    if y_type == 'minimum maximum':
        # train random forest
        model = RandomForestRegressor(verbose=2, n_estimators=100, n_jobs=-1, random_state=seed)
        model.fit(x_train, y_train)

        # make predictions using trained random forest
        y_predicted = model.predict(x_test)

        # calculate mse
        mse = mean_squared_error(y_test, y_predicted)
        print('\n\nTest MSE:', mse)

        # calculate rmse
        rmse = np.sqrt(mse)
        print('Test RMSE:', rmse)

        # calculate mae
        mae = mean_absolute_error(y_test, y_predicted)
        print('Test MAE:', mae, '\n\n')

        # get lists of actual values and predicted values for each column
        actual_max_down = np.array([i[0] for i in y_test if True], dtype=float)
        actual_max_up = np.array([i[1] for i in y_test if True], dtype=float)
        predicted_max_down = np.array([i[0] for i in y_predicted if True], dtype=float)
        predicted_max_up = np.array([i[1] for i in y_predicted if True], dtype=float)

        # plot predicted vs actual
        plt.plot(actual_max_down, label='Actual Max Down')
        plt.plot(actual_max_up, label='Actual Max Up')
        plt.plot(predicted_max_down, label='Predicted Max Down')
        plt.plot(predicted_max_up, label='Predicted Max Up')
        plt.title('Predicted vs Actual')
        plt.legend()
        save_plot_path = get_model_performance_visual_insights_path(symbol, 'Predicted vs Actual')
        plt.savefig(save_plot_path)
        if visualize_actual_vs_predicted == True and show_plots_during_training() == True:
            plt.show()
        else:
            plt.close()

        # get feature importance
        feature_importance = model.feature_importances_

        # plot feature importance
        plt.bar([x_column_list[x] for x in range(len(feature_importance))], feature_importance)
        plt.xticks(rotation=90, ha='right')
        plt.title("Feature Importance")
        plt.xlabel("Features")
        plt.ylabel("Scores")
        save_plot_path = get_model_performance_visual_insights_path(symbol, 'Feature Importance')
        plt.savefig(save_plot_path)
        if visualize_feature_importance == True and show_plots_during_training() == True:
            plt.show()
        else:
            plt.close()
    # ***************************************************************************************************************************

    # buy or sell ***************************************************************************************************************
    elif y_type == 'buy or sell':
        # make sure y_train and y_test are 1D arrays ******************************************************************
        y_train = np.ravel(y_train)
        y_test = np.ravel(y_test)
        # *************************************************************************************************************

        # actions class counts for the whole dataset ******************************************************************
        print('Actions Class Count (whole dataset):\n', dataset[y_column_list[0]].value_counts(), '\n\n')
        # *************************************************************************************************************

        # initialize label encoder ... to encode string labels to numerical labels ... xgbclassifier requirement for the target variable
        label_encoder = LabelEncoder()
        # *************************************************************************************************************

        # encode our y train and y test sets **************************************************************************
        y_train = label_encoder.fit_transform(y_train)
        y_test = label_encoder.fit_transform(y_test)
        # *************************************************************************************************************
        
        # balance classes using SMOTE *********************************************************************************
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
        # *************************************************************************************************************

        # train model *************************************************************************************************
        # get sample weights
        sample_weights = compute_sample_weight(
            class_weight='balanced',
            y=train_dataset[y_column_list[0]] # target
        )
        print('###SAMPLE WEIGHTS:\n', sample_weights, '\n\n')
        # create RF classifier model
        model = RandomForestClassifier(n_estimators = 100, verbose=2, n_jobs=-1, random_state=seed)  
        # create XGBoost classifier model
        # model = XGBClassifier(objective='multi:softprob', num_class=3, verbosity=2)
        # n_estimators = 100 default , max_depth = 3 default , , sample_weight=sample_weights

        # train model
        model.fit(x_train, y_train) # random forest doing well with sample weights supplied
        
        # performing predictions on the test dataset
        y_predicted = model.predict(x_test)
        # *************************************************************************************************************

        # decode y data back to the original string labels ************************************************************
        # decode the predictions back to the original string labels
        y_predicted = label_encoder.inverse_transform(y_predicted)
        # decode y_test back to the original string labels
        y_test = label_encoder.inverse_transform(y_test)
        # *************************************************************************************************************

        # make sure y_predicted and y_test are 1D arrays **************************************************************
        y_predicted = np.ravel(y_predicted)
        y_test = np.ravel(y_test)
        # *************************************************************************************************************

        # model perfomance ********************************************************************************************
        # using metrics module for accuracy calculation
        print('\n\nACCURACY OF THE MODEL:', accuracy_score(y_test, y_predicted), '\n\n')

        # print classification report for model
        print('CLASSIFICATION REPORT:\n', classification_report(y_test, y_predicted), '\n\n')

        # print confusion matrix
        confusion_matrix_ = pd.DataFrame(
            confusion_matrix(y_test, y_predicted, labels=[
                'Buy',
                'Nothing',
                'Sell'
            ]), 
            index=[
                'Buys',
                'Nothing',
                'Sells'
            ], 
            columns=[
                'Predicted As Buys',
                'Predicted As Nothing',
                'Predicted As Sells'
            ]
        )
        print('CONFUSION MATRIX:\n', confusion_matrix_, '\n\n')
        # *************************************************************************************************************

        # visualize actual vs predicted *******************************************************************************
        # replace all Buys with 1
        y_test[y_test == 'Buy'] = 1
        y_predicted[y_predicted == 'Buy'] = 1

        # replace all Nothing with 0
        y_test[y_test == 'Nothing'] = 0
        y_predicted[y_predicted == 'Nothing'] = 0

        # replace all Sells with -1
        y_test[y_test == 'Sell'] = -1
        y_predicted[y_predicted == 'Sell'] = -1

        # plot comparisons
        plt.plot(y_test, label='Actual')
        plt.plot(y_predicted, label='Predicted')
        plt.xticks(rotation=90)
        plt.title('Predicted vs Actual')
        plt.legend()
        save_plot_path = get_model_performance_visual_insights_path(symbol, 'Predicted vs Actual')
        plt.savefig(save_plot_path)
        if visualize_actual_vs_predicted == True and show_plots_during_training() == True:
            plt.show()
        else:
            plt.close()

        # replace all 1s with Buys
        y_test[y_test == 1] = 'Buy'
        y_predicted[y_predicted == 1] = 'Buy'

        # replace all 0s with Nothings
        y_test[y_test == 0] = 'Nothing'
        y_predicted[y_predicted == 0] = 'Nothing'

        # replace all -1s with Sells
        y_test[y_test == -1] = 'Sell'
        y_predicted[y_predicted == -1] = 'Sell'
        # *************************************************************************************************************

        # feature importance ******************************************************************************************
        # get feature importance
        feature_importance = model.feature_importances_

        # plot feature importance
        plt.bar([x_column_list[x] for x in range(len(feature_importance))], feature_importance)
        plt.xticks(rotation=90, ha='right')
        plt.title("Feature Importance")
        plt.xlabel("Features")
        plt.ylabel("Scores")
        save_plot_path = get_model_performance_visual_insights_path(symbol, 'Feature Importance')
        plt.savefig(save_plot_path)
        if visualize_feature_importance == True and show_plots_during_training() == True:
            plt.show()
        else:
            plt.close()
        # *************************************************************************************************************

        # insights on the predicted trades ****************************************************************************
        # state risk amount ... eg risking a dollar on each trade
        risk_amount = 1 # dollar(s)
        # initialize current account balance ... to get a equity graph using the predicted trades
        initial_balance = 100 # dollar(s)
        current_balance = initial_balance
        # initialize array store current balances
        current_balances = deque([])
        # initialize array to store win / lose results
        win_lose_results = deque([])
        # initialize array to store counts of consecutive wins
        consecutive_wins = deque([])
        # initialize array to store counts of consecutive losses
        consecutive_losses = deque([])
        # wins counter
        wins_counter = 0
        # losses counter
        losses_counter = 0
        # initialize array to store predicted buy prices
        predicted_buy_prices = deque([])
        # initialize array to store predicted sell prices
        predicted_sell_prices = deque([])
        # initialize array to store takeprofits for predicted trades
        takeprofits = deque([])
        # initialize array to store stoplosses for predicted trades
        stoplosses = deque([])
        # initialize array to store stoploss hit statuses
        stoploss_hit_statuses = deque([])
        # initialize array to store stoploss missed statuses
        stoploss_missed_statuses = deque([])
        # initialize array to store takeprofit missed statuses
        takeprofit_missed_statuses = deque([])
        # compare actual vs predicted and get wanted win / lose results *************************************
        for i in tqdm(range(len(y_test)), desc="Predicted Trades Insight Generation", unit="row"):
            # get actual value and predicted value
            actual = y_test[i]; predicted = y_predicted[i]
            # initialize predicted buy price with NaN
            predicted_buy_price = np.nan
            # initialize predicted sell price with NaN
            predicted_sell_price = np.nan
            # initialize takeprofit price with NaN
            takeprofit = np.nan
            # initialize stoploss price with NaN
            stoploss = np.nan
            # initialize stoploss hit variable
            stoploss_hit = False
            # initialize stoploss missed variable
            stoploss_missed = False
            # initialize takeprofit missed variable
            takeprofit_missed = False
            # if a buy or sell was predicted ******************************************************
            if predicted != 'Nothing':
                # win / lose determination **********************************************
                # if predicted action is the same as the actual action ********
                if predicted == actual:
                    # mark result as win 
                    result = 'win'
                    # update current balance
                    current_balance = current_balance + (risk_amount * risk_target_divisor)
                # *************************************************************
                # if predicted action is not the same as the actual action ****
                else: 
                    # mark result as lose
                    result = 'lose' 
                # *************************************************************
                # ***********************************************************************
                # increment corresponding counter by 1 **********************************
                if result == 'win': wins_counter = wins_counter + 1
                elif result == 'lose': losses_counter = losses_counter + 1
                # ***********************************************************************
                # get trade's closing percentage ****************************************
                trade_closing_percentage = test_trade_closing_percentages[i]
                # ***********************************************************************
                # if predicted trade is a buy *******************************************
                if predicted == 'Buy': 
                    # predicted buy price
                    predicted_buy_price = test_closes[i]
                    # takeprofit
                    takeprofit = predicted_buy_price + ((reward / 100) * predicted_buy_price)
                    # stoploss
                    stoploss = predicted_buy_price - ((risk / 100) * predicted_buy_price)
                    # check if stoploss was hit *******************************
                    # if trade was a loss ***************************
                    if result == 'lose':
                        # max percentage down
                        max_percentage_down = test_max_percentages_down[i]
                        # check stoploss hit **************
                        if max_percentage_down <= -risk:
                            # mark stoploss hit 
                            stoploss_hit = True
                            # update current balance accordingly
                            current_balance = current_balance - risk_amount 
                        # *********************************
                        # *********************************
                        # if trade closed in the negative and the stoploss wasn't hit 
                        if trade_closing_percentage <= 0 and stoploss_hit == False:
                            # mark stoploss miss
                            stoploss_missed = True
                            # update current balance accordingly
                            current_balance = current_balance - ((1 / (risk / abs(trade_closing_percentage))) * risk_amount)
                        # *********************************
                        # if trade closed in the positive and the takeprofit wasn't hit
                        if trade_closing_percentage > 0 and stoploss_hit == False:
                            # mark takeprofit missed
                            takeprofit_missed = True
                            # update current balance accordingly
                            current_balance = current_balance + ((1 / (reward / abs(trade_closing_percentage))) * (risk_amount * risk_target_divisor))
                        # *********************************
                        # *******************************************
                    # *********************************************************
                # ***********************************************************************
                # if predicted trade is a sell ******************************************
                elif predicted == 'Sell': 
                    # predicted sell price
                    predicted_sell_price = test_closes[i]
                    # takeprofit
                    takeprofit = predicted_sell_price - ((reward / 100) * predicted_sell_price)
                    # stoploss
                    stoploss = predicted_sell_price + ((risk / 100) * predicted_sell_price)
                    # check if stoploss was hit *******************************
                    # if trade was a loss ***************************
                    if result == 'lose':
                        # max percentage up
                        max_percentage_up = test_max_percentages_up[i]
                        # check stoploss hit **************
                        if max_percentage_up >= risk:
                            # mark stoploss hit 
                            stoploss_hit = True
                            # update current balance accordingly
                            current_balance = current_balance - risk_amount 
                        # *********************************
                        # *********************************
                        # if trade closed in the negative and the stoploss wasn't hit 
                        if trade_closing_percentage >= 0 and stoploss_hit == False:
                            # mark stoploss miss
                            stoploss_missed = True
                            # update current balance accordingly
                            current_balance = current_balance - ((1 / (risk / abs(trade_closing_percentage))) * risk_amount)
                        # *********************************
                        # if trade closed in the positive and the takeprofit wasn't hit
                        if trade_closing_percentage < 0 and stoploss_hit == False:
                            # mark takeprofit missed
                            takeprofit_missed = True
                            # update current balance accordingly
                            current_balance = current_balance + ((1 / (reward / abs(trade_closing_percentage))) * (risk_amount * risk_target_divisor))
                        # *********************************
                    # ***********************************************
                    # *********************************************************
                # ***********************************************************************
                # consecutive wins and losses *******************************************
                # length of win_lose_results
                win_lose_results_length = len(win_lose_results)
                # if win_lose_results array is not empty
                if win_lose_results_length > 0:
                    # get previous result
                    previous_result = win_lose_results[-1]
                    # if previous result and the current result are not the same, or we are on the last item
                    if result != previous_result:
                        # add previous result to consecutive wins/losses array using its counter, then reset the counter
                        if previous_result == 'win': consecutive_wins.append(wins_counter); wins_counter = 0
                        elif previous_result == 'lose': consecutive_losses.append(losses_counter); losses_counter = 0
                    # if we are on the last item
                    if i == len(y_test)-1:
                        # add current result to consecutive wins/losses array using its counter, then reset the counter
                        if result == 'win': consecutive_wins.append(wins_counter); wins_counter = 0
                        elif result == 'lose': consecutive_losses.append(losses_counter); losses_counter = 0
                # ***********************************************************************
                # add result to win_lose_results array **********************************
                win_lose_results.append(result)
                # ***********************************************************************
            # *************************************************************************************
            # append current balance **************************************************************
            current_balances.append(current_balance)
            # *************************************************************************************
            # append actions to their respective arrays *******************************************
            predicted_buy_prices.append(predicted_buy_price)
            predicted_sell_prices.append(predicted_sell_price)
            # *************************************************************************************
            # append takeprofits and stoplosses to their respective arrays ************************
            takeprofits.append(takeprofit)
            stoplosses.append(stoploss)
            # *************************************************************************************
            # append stoploss hit status **********************************************************
            stoploss_hit_statuses.append(stoploss_hit)
            # *************************************************************************************
            # append stoploss missed status *******************************************************
            stoploss_missed_statuses.append(stoploss_missed)
            # *************************************************************************************
            # append takeprofit missed status *****************************************************
            takeprofit_missed_statuses.append(takeprofit_missed)
            # *************************************************************************************
        # ***************************************************************************************************
        # arrays to numpy arrays ****************************************************************************
        current_balances = np.array(current_balances)
        win_lose_results = np.array(win_lose_results)
        consecutive_wins = np.array(consecutive_wins)
        consecutive_losses = np.array(consecutive_losses)
        predicted_buy_prices = np.array(predicted_buy_prices)
        predicted_sell_prices = np.array(predicted_sell_prices)
        takeprofits = np.array(takeprofits)
        stoplosses = np.array(stoplosses)
        stoploss_hit_statuses = np.array(stoploss_hit_statuses)
        stoploss_missed_statuses = np.array(stoploss_missed_statuses)
        takeprofit_missed_statuses = np.array(takeprofit_missed_statuses)
        # ***************************************************************************************************
        # get the to_trading_days_divisor based on the entry timeframe **************************************
        if timeframe == 'Daily': to_trading_days_divisor = 1
        elif timeframe == 'H4': to_trading_days_divisor = 6
        elif timeframe == 'H1': to_trading_days_divisor = 24
        elif timeframe == 'M30': to_trading_days_divisor = 48
        elif timeframe == 'M15': to_trading_days_divisor = 96
        # ***************************************************************************************************
        # insights, with Python native data types ***********************************************************
        # starting account balance
        starting_account_balance = float(initial_balance)
        # account balance after trades
        account_balance_after_trades = float(current_balance)
        # number of trades taken
        number_of_trades_taken = int(len(win_lose_results))
        # trades won
        trades_won = int(np.sum(consecutive_wins))
        # trades lost
        trades_lost = int(np.sum(consecutive_losses))
        # number of stoploss hits
        stoploss_hits = len(np.where(stoploss_hit_statuses == True)[0])
        # number of stoploss misses
        stoploss_misses = len(np.where(stoploss_missed_statuses == True)[0])
        # number of takeprofit misses
        takeprofit_misses = len(np.where(takeprofit_missed_statuses == True)[0])
        # overall win rate
        overall_win_rate = float((len(np.where(win_lose_results == 'win')[0]) / len(win_lose_results)) * 100)
        # maximum number of consecutive wins
        maximum_number_of_consecutive_wins = int(np.max(consecutive_wins))
        # maximum number of consecutive losses
        maximum_number_of_consecutive_losses = int(np.max(consecutive_losses))
        # average number of consecutive wins
        average_number_of_consecutive_wins = float(np.mean(consecutive_wins))
        # average number of consecutive losses
        average_number_of_consecutive_losses = float(np.mean(consecutive_losses))
        # number of features
        number_of_features = int(x_train.shape[1])
        # training data start date
        training_data_start_date = str(train_dates[0])
        # training data end date
        training_data_end_date = str(train_dates[-1])
        # training data number of trading days
        training_data_number_of_trading_days = float(len(train_dataset) / to_trading_days_divisor)
        # test data start date
        test_data_start_date = str(test_dates[0])
        # test data end date
        test_data_end_date = str(test_dates[-1])
        # test data number of trading days
        test_data_number_of_trading_days = float(len(test_dataset) / to_trading_days_divisor)
        # win / lose results, list
        win_lose_results = win_lose_results.tolist()
        # consecutive wins, list
        consecutive_wins = consecutive_wins.tolist()
        # consecutive losses, list
        consecutive_losses = consecutive_losses.tolist()
        # balances, list
        balances = current_balances.tolist()
        # ***************************************************************************************************
        # print out insight on the predicted trades *********************************************************
        print('\n\nStarting account balance (example in $):', starting_account_balance)
        print('Account balance after trades ($):', account_balance_after_trades)
        print('Number of trades taken:', number_of_trades_taken)
        print('Trades won:', trades_won)
        print('Trades lost:', trades_lost)
        print('Overall Win Rate %:', overall_win_rate)
        print('Risk:Reward:', risk_to_reward_ratio)
        print('Stoploss Hits:', stoploss_hits)
        print('Stoploss Misses:', stoploss_misses)
        print('Takeprofit Misses:', takeprofit_misses)
        print('Maximum number of consecutive wins:', maximum_number_of_consecutive_wins)
        print('Maximum number of consecutive losses:', maximum_number_of_consecutive_losses)
        print('Average number of consecutive wins:', average_number_of_consecutive_wins)
        print('Average number of consecutive losses:', average_number_of_consecutive_losses)
        print('Number of features:', number_of_features)
        print('Training data start date:', training_data_start_date)
        print('Training data end date:', training_data_end_date)
        print('Training data number of days:', training_data_number_of_trading_days)
        print('Test data start date:', test_data_start_date)
        print('Test data end date:', test_data_end_date)
        print('Test data number of days:', test_data_number_of_trading_days)
        print('Win / Lose Results:', win_lose_results)
        print('Consecutive wins:', consecutive_wins)
        print('Consecutive losses:', consecutive_losses)
        print('Balances ($):', balances)
        # ***************************************************************************************************
        # *************************************************************************************************************

        # make sure test dates are compatible with matplotlib *********************************************************
        test_dates = np.array(test_dates, dtype=str)
        test_dates = [mdates.datestr2num(date) for date in test_dates] # convert test_dates to matplotlib date format
        # *************************************************************************************************************

        # equity graph ************************************************************************************************
        # plot equity graph
        plt.plot(current_balances, label='Balance ($)')
        plt.xticks(rotation=90)
        plt.title('Account Balance')
        plt.legend()
        save_plot_path = get_model_performance_visual_insights_path(symbol, 'Account Balance')
        plt.savefig(save_plot_path)
        if visualize_equity_graph == True and show_plots_during_training() == True:
            plt.show()
        else:
            plt.close()
        # *************************************************************************************************************

        # ohlc buy sell graph *****************************************************************************************
        # combine data into OHLC format
        ohlc = np.array([[test_dates[i], test_opens[i], test_highs[i], test_lows[i], test_closes[i]] for i in range(len(test_dates))])

        # plotting
        fig, ax = plt.subplots(figsize=(10, 6))

        # plot OHLC data
        candlestick_ohlc(ax, ohlc, width=0.0003, colorup='green', colordown='red')

        # plot predicted buying and selling points as dots (scatter)
        ax.scatter(test_dates, predicted_buy_prices, label='Predicted Buys', color='blue', marker='o', s=5)
        ax.scatter(test_dates, predicted_sell_prices, label='Predicted Sells', color='maroon', marker='o', s=5)

        # plot takeprofit and stoploss points for predicted trades as dots (scatter)
        ax.scatter(test_dates, takeprofits, label='Takeprofits', color='green', marker='o', s=5)
        ax.scatter(test_dates, stoplosses, label='Stoplosses', color='red', marker='o', s=5)

        # formatting the x-axis
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=len(test_dates))) # set a custom locator to customize the number of ticks

        # set x-axis limits to ensure proper spacing
        ax.set_xlim(test_dates[0] - 0.5, test_dates[-1] + 0.5)

        # plot parameters
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(symbol + 'Buy Sell OHLC Chart')
        plt.legend(loc="upper right")
        # plt.grid()
        plt.xticks(rotation=90)
        plt.tight_layout()
        save_plot_path = get_model_performance_visual_insights_path(symbol, 'Buy Sell OHLC Chart')
        plt.savefig(save_plot_path)
        if visualize_ohlc_buy_sell_graph == True and show_plots_during_training() == True:
            plt.show()
        else:
            plt.close()
        # *************************************************************************************************************
    # ***************************************************************************************************************************

    # # pickle scaler *************************************************************************************************************
    # pickled_scaler = pickle.dumps(scaler)
    # # ***************************************************************************************************************************

    # # pickle model **************************************************************************************************************
    # pickled_model = pickle.dumps(model)
    # # ***************************************************************************************************************************

    # # initialize fernet object using the encryption key *************************************************************************
    # # encryption key variable will be contained in the module that will decrypt and run this code, the key will automatically become part of this module
    # fernet = Fernet(key)
    # # ***************************************************************************************************************************

    # # encrypt pickled scaler ****************************************************************************************************
    # encrypted_pickled_scaler = fernet.encrypt(pickled_scaler)
    # # ***************************************************************************************************************************

    # # encrypt pickled model *****************************************************************************************************
    # encrypted_pickled_model = fernet.encrypt(pickled_model)
    # # ***************************************************************************************************************************

    # # save encrypted scaler *****************************************************************************************************
    # # scaler path
    # scaler_path = get_scaler_path(symbol)
    # # save encrypted pickled scaler file to scaler path
    # with open(scaler_path, 'wb') as file:
    #     file.write(encrypted_pickled_scaler)
    # # ***************************************************************************************************************************

    # # save encrypted model ******************************************************************************************************
    # # model path
    # model_path = get_model_path(symbol)
    # # save encrypted pickled model file to model path 
    # with open(model_path, 'wb') as file:
    #     file.write(encrypted_pickled_model)
    # # ***************************************************************************************************************************

    # generate training log (json) **********************************************************************************************
    training_log = {
        "Symbol":  symbol,
        "Starting account balance (example in $)": starting_account_balance,
        "Account balance after trades ($)": account_balance_after_trades,
        "Number of trades taken": number_of_trades_taken,
        "Trades won": trades_won,
        "Trades lost": trades_lost,
        "Overall Win Rate %": overall_win_rate,
        "Risk:Reward": risk_to_reward_ratio,
        "Stoploss Hits": stoploss_hits,
        "Stoploss Misses": stoploss_misses,
        "Takeprofit Misses": takeprofit_misses,
        "Maximum number of consecutive wins": maximum_number_of_consecutive_wins,
        "Maximum number of consecutive losses": maximum_number_of_consecutive_losses,
        "Average number of consecutive wins": average_number_of_consecutive_wins,
        "Average number of consecutive losses": average_number_of_consecutive_losses,
        "Number of features": number_of_features,
        "Training data start date": training_data_start_date,
        "Training data end date": training_data_end_date,
        "Training data number of trading days": training_data_number_of_trading_days,
        "Test data start date": test_data_start_date,
        "Test data end date": test_data_end_date,
        "Test data number of trading days": test_data_number_of_trading_days,
        "Win / Lose Results": win_lose_results,
        "Consecutive wins": consecutive_wins,
        "Consecutive losses": consecutive_losses,
        "Balances ($)": balances
    }
    # training logs json
    training_logs_json = json.dumps(training_log, indent=4)
    # ***************************************************************************************************************************

    # save training log *********************************************************************************************************
    # training logs path
    training_logs_path = get_training_log_path(symbol)
    # save training logs json file to training logs path
    with open(training_logs_path, 'w') as file:
        file.write(training_logs_json)
    # ***************************************************************************************************************************

    # signal the end of the current symbol's model training
    print('\n\n', symbol, 'Model Training Complete.\n\n')
# *****************************************************************************************************************************************