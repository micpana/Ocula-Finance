import numpy as np
from collections import deque
from tqdm import tqdm
from symbol_config import get_symbol_list, get_symbol_config
from settings import predictions_filter_config, test_predictions_result_arrays_printing_config
from minutes_to_hours_and_minutes import minutes_to_hours_and_minutes

# filtering predictions using a probability threshold *************************************************************************************
filter_predictions_using_a_probability_threshold, prediction_probability_threshold = predictions_filter_config()
# *****************************************************************************************************************************************

# get trade outcome ***********************************************************************************************************************
def get_trade_outcome(
        predicted_trade_action, predicted_trade_stoploss_percentage, predicted_trade_takeprofit_percentage,  
        actual_trade_action, trade_maximum_percentage_up, trade_maximum_percentage_down, trade_session_closing_percentage
    ):
    # if trade was a win **********************************************************************************************
    if predicted_trade_action == actual_trade_action:
        # set takeprofit hit to true
        takeprofit_hit = True
        # set stoploss hit to false
        stoploss_hit = False
        # set trade closing percentage
        trade_close_percentage = predicted_trade_takeprofit_percentage
        # set trade won to true
        trade_won = True
    # *****************************************************************************************************************
    # if trade was a lose *********************************************************************************************
    else:
        # set takeprofit hit to false
        takeprofit_hit = False
        # set trade won to false
        trade_won = False
        # check if stoploss was hit or not ******************************************************************
        # for buys ********************************************************************************
        if predicted_trade_action == 'Buy': 
            if trade_maximum_percentage_down <= predicted_trade_stoploss_percentage: stoploss_hit = True; trade_close_percentage = predicted_trade_stoploss_percentage
            else: stoploss_hit = False; trade_close_percentage = trade_session_closing_percentage
        # *****************************************************************************************
        # for sells *******************************************************************************
        if predicted_trade_action == 'Sell': 
            if trade_maximum_percentage_up >= predicted_trade_stoploss_percentage: stoploss_hit = True; trade_close_percentage = predicted_trade_stoploss_percentage
            else: stoploss_hit = False; trade_close_percentage = trade_session_closing_percentage
        # *****************************************************************************************
        # ***************************************************************************************************
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # return takeprofit_hit, stoploss_hit, trade_close_percentage, trade_won
    return takeprofit_hit, stoploss_hit, trade_close_percentage, trade_won
# *****************************************************************************************************************************************

# get trade outcomes **********************************************************************************************************************
def get_trade_outcomes(
        symbol, entry_timeframe_minutes_in_a_single_bar, test_closes, test_trade_closing_percentages, test_max_percentages_down, 
        test_max_percentages_up, y_test, y_predicted, y_predicted_probabilities
    ):
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
                
    # forecast period
    forecast_period = symbol_config['forecast_period']
    
    # holding period
    holding_period = symbol_config['holding_period']

    # symbol type
    symbol_type = symbol_config['type']
    # ***************************************************************************************************************************

    # get insights on the predicted trades **************************************************************************************
    # initialize variables for actual trades **************************************************************************
    # initialize array to store actual buy prices
    actual_buy_prices = deque([])
    # initialize array to store actual sell prices
    actual_sell_prices = deque([])
    # initialize array to store takeprofits for actual trades
    actual_takeprofits = deque([])
    # initialize array to store stoplosses for actual trades
    actual_stoplosses = deque([])
    # *****************************************************************************************************************
    # initialize variables for predicted trades ***********************************************************************
    # state risk amount ... eg risking a dollar on each trade
    risk_amount = 1 # dollar(s)
    # state initial account balance
    initial_balance = 100 # dollar(s)
    # initialize current account balance ... to get a equity graph using the predicted trades
    current_balance = initial_balance
    # initialize array store current balances
    current_balances = deque([])
    # initialize array to store outcomes for predicted actions, ie win / lose / nothing
    predicted_actions_outcomes = deque([])
    # initialize array to store win / lose results
    win_lose_results = deque([])
    # initialize array to store counts of consecutive wins
    consecutive_wins = deque([])
    # initialize array to store counts of consecutive losses
    consecutive_losses = deque([])
    # initialize array to store waiting times in minutes, ie, time inbetween trades
    waiting_times_in_minutes = deque([])
    # wins counter
    wins_counter = 0
    # losses counter
    losses_counter = 0
    # waiting time count in minutes
    waiting_time_count_in_minutes = 0
    # initialize array to store predicted buy prices
    predicted_buy_prices = deque([])
    # initialize array to store predicted sell prices
    predicted_sell_prices = deque([])
    # initialize array to store takeprofits for predicted trades
    predicted_takeprofits = deque([])
    # initialize array to store stoplosses for predicted trades
    predicted_stoplosses = deque([])
    # initialize array to store stoploss hit statuses
    stoploss_hit_statuses = deque([])
    # initialize array to store stoploss missed statuses
    stoploss_missed_statuses = deque([])
    # initialize array to store takeprofit missed statuses
    takeprofit_missed_statuses = deque([])
    # *****************************************************************************************************************
    # compare actual vs predicted and get wanted win / lose results ***************************************************
    for i in tqdm(range(len(y_test)), desc="Predicted Trades Insight Generation", unit="row"):
        # initialize loop's actual trades variables *********************************************************
        # initialize actual buy price with NaN
        actual_buy_price = np.nan
        # initialize actual sell price with NaN
        actual_sell_price = np.nan
        # initialize actual takeprofit price with NaN
        actual_takeprofit = np.nan
        # initialize actual stoploss price with NaN
        actual_stoploss = np.nan
        # ***************************************************************************************************
        # initialize loop's predicted trades variables ******************************************************
        # initialize predicted buy price with NaN
        predicted_buy_price = np.nan
        # initialize predicted sell price with NaN
        predicted_sell_price = np.nan
        # initialize predicted takeprofit price with NaN
        predicted_takeprofit = np.nan
        # initialize predicted stoploss price with NaN
        predicted_stoploss = np.nan
        # initialize stoploss hit variable
        stoploss_hit = False
        # initialize stoploss missed variable
        stoploss_missed = False
        # initialize takeprofit missed variable
        takeprofit_missed = False
        # ***************************************************************************************************

        # get actual value and predicted value, plus the predicted probabilities, and the max predicted probability (max predicted probability is the probability of the predicted class)
        actual = y_test[i]; predicted = y_predicted[i]; predicted_probabilities = y_predicted_probabilities[i]; max_predicted_probability = np.max(predicted_probabilities)
        # ***************************************************************************************************

        # if the actual trade is a buy or sell **************************************************************
        if actual != 'Nothing':
            # if actual trade is a buy ************************************************************
            if actual == 'Buy':
                # actual buy price
                actual_buy_price = test_closes[i]
                # actual takeprofit
                actual_takeprofit = actual_buy_price + ((reward / 100) * actual_buy_price)
                # actual stoploss
                actual_stoploss = actual_buy_price - ((risk / 100) * actual_buy_price)
            # *************************************************************************************
            # if actual trade is a sell ***********************************************************
            elif actual == 'Sell':
                # actual sell price
                actual_sell_price = test_closes[i]
                # actual takeprofit
                actual_takeprofit = actual_sell_price - ((reward / 100) * actual_sell_price)
                # actual stoploss
                actual_stoploss = actual_sell_price + ((risk / 100) * actual_sell_price)
            # *************************************************************************************
        # ***************************************************************************************************

        # if a buy or sell was predicted, and its probability matches our criteria **************************
        if predicted != 'Nothing' and ((filter_predictions_using_a_probability_threshold == False) or (filter_predictions_using_a_probability_threshold == True and max_predicted_probability >= prediction_probability_threshold)):
            # win / lose determination ************************************************************
            # if predicted action is the same as the actual action ********************************
            # mark result as win and update current balance
            if predicted == actual: result = 'win'; current_balance = current_balance + (risk_amount * risk_target_divisor)
            # *************************************************************************************
            # if predicted action is not the same as the actual action ****************************
            else: result = 'lose' # mark result as lose
            # *************************************************************************************
            # *************************************************************************************
            # increment corresponding counter by 1 ************************************************
            if result == 'win': wins_counter = wins_counter + 1
            elif result == 'lose': losses_counter = losses_counter + 1
            # *************************************************************************************
            # get trade's closing percentage ******************************************************
            trade_closing_percentage = test_trade_closing_percentages[i]
            # *************************************************************************************
            # if predicted trade is a buy *********************************************************
            if predicted == 'Buy': 
                # predicted buy price
                predicted_buy_price = test_closes[i]
                # predicted takeprofit
                predicted_takeprofit = predicted_buy_price + ((reward / 100) * predicted_buy_price)
                # predicted stoploss
                predicted_stoploss = predicted_buy_price - ((risk / 100) * predicted_buy_price)
                # check if stoploss was hit *********************************************
                # if trade was a loss *****************************************
                if result == 'lose':
                    # max percentage down
                    max_percentage_down = test_max_percentages_down[i]
                    # check stoploss hit ****************************
                    if max_percentage_down <= -risk:
                        # mark stoploss hit 
                        stoploss_hit = True
                        # balance change
                        balance_change = -risk_amount # negative change
                    # ***********************************************
                    # ***********************************************
                    # if trade closed in the negative and the stoploss wasn't hit 
                    if trade_closing_percentage <= 0 and stoploss_hit == False:
                        # mark stoploss miss
                        stoploss_missed = True
                        # balance change
                        balance_change = -((1 / (risk / abs(trade_closing_percentage))) * risk_amount) # negative change
                    # ***********************************************
                    # if trade closed in the positive and the takeprofit wasn't hit
                    if trade_closing_percentage > 0 and stoploss_hit == False:
                        # mark takeprofit missed
                        takeprofit_missed = True
                        # balance change
                        balance_change = ((1 / (reward / abs(trade_closing_percentage))) * (risk_amount * risk_target_divisor)) # positive change
                    # ***********************************************
                    # update current balance accordingly ************
                    current_balance = current_balance + balance_change
                    # ***********************************************
                # *************************************************************
                # ***********************************************************************
            # *************************************************************************************
            # if predicted trade is a sell ********************************************************
            elif predicted == 'Sell': 
                # predicted sell price
                predicted_sell_price = test_closes[i]
                # predicted takeprofit
                predicted_takeprofit = predicted_sell_price - ((reward / 100) * predicted_sell_price)
                # predicted stoploss
                predicted_stoploss = predicted_sell_price + ((risk / 100) * predicted_sell_price)
                # check if stoploss was hit *********************************************
                # if trade was a loss *****************************************
                if result == 'lose':
                    # max percentage up
                    max_percentage_up = test_max_percentages_up[i]
                    # check stoploss hit ****************************
                    if max_percentage_up >= risk:
                        # mark stoploss hit 
                        stoploss_hit = True
                        # balance change
                        balance_change = -risk_amount # negative change
                    # ***********************************************
                    # ***********************************************
                    # if trade closed in the negative and the stoploss wasn't hit 
                    if trade_closing_percentage >= 0 and stoploss_hit == False:
                        # mark stoploss miss
                        stoploss_missed = True
                        # balance change
                        balance_change = -((1 / (risk / abs(trade_closing_percentage))) * risk_amount) # negative change
                    # ***********************************************
                    # if trade closed in the positive and the takeprofit wasn't hit
                    if trade_closing_percentage < 0 and stoploss_hit == False:
                        # mark takeprofit missed
                        takeprofit_missed = True
                        # balance change
                        balance_change = ((1 / (reward / abs(trade_closing_percentage))) * (risk_amount * risk_target_divisor)) # positive change
                    # ***********************************************
                    # update current balance accordingly*************
                    current_balance = current_balance + balance_change
                    # ***********************************************
                # *************************************************************
                # ***********************************************************************
            # *************************************************************************************
            # consecutive wins and losses *********************************************************
            # length of win_lose_results
            win_lose_results_length = len(win_lose_results)
            # if win_lose_results array is not empty
            if win_lose_results_length > 0:
                # get previous result
                previous_result = win_lose_results[-1]
                # if previous result and the current result are not the same
                if result != previous_result:
                    # add previous result to consecutive wins/losses array using its counter, then reset the counter
                    if previous_result == 'win': consecutive_wins.append(wins_counter); wins_counter = 0
                    elif previous_result == 'lose': consecutive_losses.append(losses_counter); losses_counter = 0
                # if we are on the last item
                if i == len(y_test)-1:
                    # add current result to consecutive wins/losses array using its counter, then reset the counter
                    if result == 'win': consecutive_wins.append(wins_counter); wins_counter = 0
                    elif result == 'lose': consecutive_losses.append(losses_counter); losses_counter = 0
            # *************************************************************************************
            # add predicted action to outcomes for predicted actions ******************************
            predicted_actions_outcomes.append(result) # ie result ('win' / 'lose') for Buys and Sells, 'nothing' for Nothings
            # *************************************************************************************
            # add result to win_lose_results array ************************************************
            win_lose_results.append(result)
            # *************************************************************************************
            # waiting time ************************************************************************
            # add current waiting_time_count_in_minutes to waiting_times_in_minutes 
            waiting_times_in_minutes.append(waiting_time_count_in_minutes)
            # reset waiting_time_count_in_minutes
            waiting_time_count_in_minutes = 0
            # *************************************************************************************
        # ***************************************************************************************************
        # no trade ******************************************************************************************
        else:
            # consecutive wins and losses *********************************************************
            # if we are on the last item
            if i == len(y_test)-1:
                # if we have an active wins / losses counter, add the counter result to consecutive wins/losses array, then reset the counter
                if wins_counter > 0: consecutive_wins.append(wins_counter); wins_counter = 0
                elif losses_counter > 0: consecutive_losses.append(losses_counter); losses_counter = 0
            # *************************************************************************************
            # add predicted action to outcomes for predicted actions ******************************
            predicted_actions_outcomes.append('nothing') # ie result ('win' / 'lose') for Buys and Sells, 'nothing' for Nothings
            # *************************************************************************************
            # waiting time ************************************************************************
            # add current bar's time in mutes to waiting_time_count_in_minutes
            waiting_time_count_in_minutes = waiting_time_count_in_minutes + entry_timeframe_minutes_in_a_single_bar
            # if we are on the last item
            if i == len(y_test)-1:
                # add current waiting_time_count_in_minutes to waiting_times_in_minutes
                waiting_times_in_minutes.append(waiting_time_count_in_minutes)
                # reset waiting_time_count_in_minutes
                waiting_time_count_in_minutes = 0
            # *************************************************************************************
        # *****************************************************************************************
        # append actual buy and sell prices to their respective arrays ****************************
        actual_buy_prices.append(actual_buy_price)
        actual_sell_prices.append(actual_sell_price)
        # *****************************************************************************************
        # append actual takeprofits and stoplosses to their respective arrays *********************
        actual_takeprofits.append(actual_takeprofit)
        actual_stoplosses.append(actual_stoploss)
        # *****************************************************************************************
        # append current balance ******************************************************************
        current_balances.append(current_balance)
        # *****************************************************************************************
        # append predicted buy and sell prices to their respective arrays *************************
        predicted_buy_prices.append(predicted_buy_price)
        predicted_sell_prices.append(predicted_sell_price)
        # *****************************************************************************************
        # append predicted takeprofits and stoplosses to their respective arrays ******************
        predicted_takeprofits.append(predicted_takeprofit)
        predicted_stoplosses.append(predicted_stoploss)
        # *****************************************************************************************
        # append stoploss hit status **************************************************************
        stoploss_hit_statuses.append(stoploss_hit)
        # *****************************************************************************************
        # append stoploss missed status ***********************************************************
        stoploss_missed_statuses.append(stoploss_missed)
        # *****************************************************************************************
        # append takeprofit missed status *********************************************************
        takeprofit_missed_statuses.append(takeprofit_missed)
        # *****************************************************************************************
    # *******************************************************************************************************
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # arrays to numpy arrays ****************************************************************************************************
    actual_buy_prices = np.array(actual_buy_prices)
    actual_sell_prices = np.array(actual_sell_prices)
    actual_takeprofits = np.array(actual_takeprofits)
    actual_stoplosses = np.array(actual_stoplosses)
    current_balances = np.array(current_balances)
    predicted_actions_outcomes = np.array(predicted_actions_outcomes)
    win_lose_results = np.array(win_lose_results)
    consecutive_wins = np.array(consecutive_wins)
    consecutive_losses = np.array(consecutive_losses)
    predicted_buy_prices = np.array(predicted_buy_prices)
    predicted_sell_prices = np.array(predicted_sell_prices)
    predicted_takeprofits = np.array(predicted_takeprofits)
    predicted_stoplosses = np.array(predicted_stoplosses)
    stoploss_hit_statuses = np.array(stoploss_hit_statuses)
    stoploss_missed_statuses = np.array(stoploss_missed_statuses)
    takeprofit_missed_statuses = np.array(takeprofit_missed_statuses)
    waiting_times_in_minutes = np.array(waiting_times_in_minutes)
    # ***************************************************************************************************************************

    # return actual_buy_prices, actual_sell_prices, actual_takeprofits, actual_stoplosses, filter_predictions_using_a_probability_threshold, prediction_probability_threshold, initial_balance, current_balance, current_balances, predicted_actions_outcomes, win_lose_results, consecutive_wins, consecutive_losses, predicted_buy_prices, predicted_sell_prices, predicted_takeprofits, predicted_stoplosses, stoploss_hit_statuses, stoploss_missed_statuses, takeprofit_missed_statuses, waiting_times_in_minutes
    return actual_buy_prices, actual_sell_prices, actual_takeprofits, actual_stoplosses, filter_predictions_using_a_probability_threshold, prediction_probability_threshold, initial_balance, current_balance, current_balances, predicted_actions_outcomes, win_lose_results, consecutive_wins, consecutive_losses, predicted_buy_prices, predicted_sell_prices, predicted_takeprofits, predicted_stoplosses, stoploss_hit_statuses, stoploss_missed_statuses, takeprofit_missed_statuses, waiting_times_in_minutes
# *****************************************************************************************************************************************

# predicted trades statistics *************************************************************************************************************
def get_predicted_trades_statistics(
        symbol, entry_timeframe, entry_timeframe_minutes_in_a_single_bar, train_dates, test_dates, x_test_shape, 
        train_dataset_length, test_dataset_length, initial_balance, current_balance, current_balances, predicted_actions_outcomes, 
        win_lose_results, consecutive_wins, consecutive_losses, predicted_buy_prices, predicted_sell_prices, takeprofits, stoplosses, 
        stoploss_hit_statuses, stoploss_missed_statuses, takeprofit_missed_statuses, waiting_times_in_minutes
    ):
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
                
    # forecast period
    forecast_period = symbol_config['forecast_period']
    
    # holding period
    holding_period = symbol_config['holding_period']

    # symbol type
    symbol_type = symbol_config['type']
    # ***************************************************************************************************************************

    # trade holding time metrics ************************************************************************************************
    # maximum trade holding time in minutes
    maximum_trade_holding_time_in_minutes = entry_timeframe_minutes_in_a_single_bar * holding_period

    # maximum holding time in hours and minutes (string)
    maximum_trade_holding_time_in_hours_and_minutes = minutes_to_hours_and_minutes(maximum_trade_holding_time_in_minutes)
    # ***************************************************************************************************************************

    # get the to_trading_days_divisor based on the entry timeframe **************************************************************
    if entry_timeframe == 'Daily': to_trading_days_divisor = 1
    elif entry_timeframe == 'H4': to_trading_days_divisor = 6
    elif entry_timeframe == 'H1': to_trading_days_divisor = 24
    elif entry_timeframe == 'M30': to_trading_days_divisor = 48
    elif entry_timeframe == 'M15': to_trading_days_divisor = 96
    elif entry_timeframe == 'M5': to_trading_days_divisor = 288
    elif entry_timeframe == 'M1': to_trading_days_divisor = 1440
    # ***************************************************************************************************************************

    # win rates for each quarter ************************************************************************************************
    # number of quarters
    number_of_quarters = 4
    # quarter length /  number of items in a quarter
    quarter_length = len(predicted_actions_outcomes) // number_of_quarters # perform floor division
    # initialize string for storing combined win rates for each quarter
    win_rates_for_each_quarter = ''
    # calculate win rate for each quarter *****************************************************************************
    for i in range(number_of_quarters):
        # quarter's outcomes for predicted actions data
        quarter_data = predicted_actions_outcomes[i * quarter_length: (i + 1) * quarter_length] # the math is simply start:end
        # quarter's win / lose results
        quarter_win_lose_results = quarter_data[(quarter_data == 'win') | (quarter_data == 'lose')]
        # quarter's number of trades
        quater_number_of_trades = len(quarter_win_lose_results)
        # number of wins
        win_count = np.count_nonzero(quarter_win_lose_results == 'win')
        # win rate
        win_rate = (win_count / quater_number_of_trades) * 100 if quater_number_of_trades > 0 else 0
        # string append value
        string_append_value = " | " if i < number_of_quarters-1 else ''
        # add quater data to win_rates_for_each_quarter string
        win_rates_for_each_quarter = win_rates_for_each_quarter + f"Q{i+1} -> {win_rate:.2f}%" + string_append_value
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # insights, with Python native data types ***********************************************************************************
    # starting account balance
    starting_account_balance = float(initial_balance)
    # account balance after trades
    account_balance_after_trades = float(current_balance)
    # number of trades taken
    number_of_trades_taken = int(len(win_lose_results))
    # trades won
    trades_won = int(len(np.where(win_lose_results == 'win')[0]))
    # trades lost
    trades_lost = int(len(np.where(win_lose_results == 'lose')[0]))
    # trades still open on training completion
    trades_still_open_on_training_completion = int(number_of_trades_taken - (trades_won + trades_lost))
    # number of stoploss hits
    stoploss_hits = int(len(np.where(stoploss_hit_statuses == True)[0]))
    # number of stoploss misses
    stoploss_misses = int(len(np.where(stoploss_missed_statuses == True)[0]))
    # number of takeprofit misses
    takeprofit_misses = int(len(np.where(takeprofit_missed_statuses == True)[0]))
    # overall win rate
    overall_win_rate = float((len(np.where(win_lose_results == 'win')[0]) / len(win_lose_results)) * 100) if len(win_lose_results) > 0 else 0
    # maximum number of consecutive wins
    maximum_number_of_consecutive_wins = int(np.max(consecutive_wins)) if len(consecutive_wins) > 0 else 0
    # number of times the maximum number of consecutive wins occured
    number_of_times_the_maximum_number_of_consecutive_wins_occured = int(len(np.where(consecutive_wins == maximum_number_of_consecutive_wins)[0]))
    # maximum number of consecutive losses
    maximum_number_of_consecutive_losses = int(np.max(consecutive_losses)) if len(consecutive_losses) > 0 else 0
    # number of times the maximum number of consecutive losses occured
    number_of_times_the_maximum_number_of_consecutive_losses_occured = int(len(np.where(consecutive_losses == maximum_number_of_consecutive_losses)[0]))
    # average number of consecutive wins
    average_number_of_consecutive_wins = float(np.mean(consecutive_wins)) if len(consecutive_wins) > 0 else 0
    # average number of consecutive losses
    average_number_of_consecutive_losses = float(np.mean(consecutive_losses)) if len(consecutive_losses) > 0 else 0
    # maximum waiting time without a trade, in hours and minutes
    maximum_waiting_time_without_a_trade_in_hours_and_minutes = minutes_to_hours_and_minutes(np.max(waiting_times_in_minutes) if len(waiting_times_in_minutes) > 0 else 0)
    # average waiting time without a trade, in hours and minutes
    average_waiting_time_without_a_trade_in_hours_and_minutes = minutes_to_hours_and_minutes(np.mean(waiting_times_in_minutes) if len(waiting_times_in_minutes) > 0 else 0)
    # minimum waiting time without a trade, in hours and minutes
    minimum_waiting_time_without_a_trade_in_hours_and_minutes = minutes_to_hours_and_minutes(np.min(waiting_times_in_minutes) if len(waiting_times_in_minutes) > 0 else 0)
    # number of features
    number_of_features = int(x_test_shape[1])
    # training data start date ... backtests will give None for train_dates
    training_data_start_date = str(train_dates[0]) if train_dates is not None else 'N/A in Backtests'
    # training data end date ... backtests will give None for train_dates
    training_data_end_date = str(train_dates[-1]) if train_dates is not None else 'N/A in Backtests'
    # training data number of trading days ... backtests will give None for train_dataset_length
    training_data_number_of_trading_days = float(train_dataset_length / to_trading_days_divisor) if train_dataset_length != None else 'N/A in Backtests'
    # test data start date
    test_data_start_date = str(test_dates[0])
    # test data end date
    test_data_end_date = str(test_dates[-1])
    # test data number of trading days
    test_data_number_of_trading_days = float(test_dataset_length / to_trading_days_divisor)
    # predicted actions' outcomes
    predicted_actions_outcomes = predicted_actions_outcomes.tolist()
    # win / lose results, list
    win_lose_results = win_lose_results.tolist()
    # consecutive wins, list
    consecutive_wins = consecutive_wins.tolist()
    # consecutive losses, list
    consecutive_losses = consecutive_losses.tolist()
    # waiting times in minutes, list
    waiting_times_in_minutes = waiting_times_in_minutes.tolist()
    # balances, list
    balances = current_balances.tolist()
    # ***************************************************************************************************************************

    # config for printing test predictions result arrays ************************************************************************
    print_predicted_actions_outcomes_array, print_win_lose_results_array, print_consecutive_wins_array, print_consecutive_losses_array, print_waiting_times_array, print_balances_array = test_predictions_result_arrays_printing_config()
    # ***************************************************************************************************************************

    # print out insight on the predicted trades *********************************************************************************
    print('\n\nSymbol:', symbol)
    print('Symbol Type:', symbol_type)
    print('Filter predictions using probability threshold:', filter_predictions_using_a_probability_threshold)
    print('Probability Threshold:',  prediction_probability_threshold)
    print('Starting account balance (example in $):', starting_account_balance)
    print('Account balance after trades ($):', account_balance_after_trades)
    print('Number of trades taken:', number_of_trades_taken)
    print('Maximum holding time for each trade:', maximum_trade_holding_time_in_hours_and_minutes)
    print('Trades won:', trades_won)
    print('Trades lost:', trades_lost)
    print('Trades still open on training completion:', trades_still_open_on_training_completion)
    print('Overall Win Rate %:', overall_win_rate)
    print('% Win Rates for each quarter in the test data:', win_rates_for_each_quarter)
    print('Risk %:', risk)
    print('Reward %:', reward)
    print('Risk:Reward:', risk_to_reward_ratio)
    print('Stoploss Hits:', stoploss_hits)
    print('Stoploss Misses:', stoploss_misses)
    print('Takeprofit Misses:', takeprofit_misses)
    print('Average number of consecutive wins:', average_number_of_consecutive_wins)
    print('Average number of consecutive losses:', average_number_of_consecutive_losses)
    print('Maximum number of consecutive wins:', maximum_number_of_consecutive_wins)
    print('Maximum number of consecutive wins occured (n times):', number_of_times_the_maximum_number_of_consecutive_wins_occured)
    print('Maximum number of consecutive losses:', maximum_number_of_consecutive_losses)
    print('Maximum number of consecutive losses occured (n times):', number_of_times_the_maximum_number_of_consecutive_losses_occured)
    print('Maximum waiting time without a trade:', maximum_waiting_time_without_a_trade_in_hours_and_minutes)
    print('Average waiting time without a trade:', average_waiting_time_without_a_trade_in_hours_and_minutes)
    print('Minimum waiting time without a trade:', minimum_waiting_time_without_a_trade_in_hours_and_minutes)
    print('Number of features:', number_of_features)
    print('Training data start date:', training_data_start_date)
    print('Training data end date:', training_data_end_date)
    print('Training data number of days:', training_data_number_of_trading_days)
    print('Test data start date:', test_data_start_date)
    print('Test data end date:', test_data_end_date)
    print('Test data number of days:', test_data_number_of_trading_days)
    if print_win_lose_results_array == True: print('Win / Lose Results:', win_lose_results)
    if print_consecutive_wins_array == True: print('Consecutive wins:', consecutive_wins)
    if print_consecutive_losses_array == True: print('Consecutive losses:', consecutive_losses)
    if print_waiting_times_array == True: print('Waiting times in minutes:', waiting_times_in_minutes)
    if print_balances_array == True: print('Balances ($):', balances)
    if print_predicted_actions_outcomes_array == True: print("Predicted Actions' Outcomes", predicted_actions_outcomes)
    # ***************************************************************************************************************************

    # return maximum_trade_holding_time_in_hours_and_minutes, symbol, symbol_type, starting_account_balance, account_balance_after_trades, number_of_trades_taken, maximum_trade_holding_time_in_hours_and_minutes, trades_won, trades_lost, trades_still_open_on_training_completion, overall_win_rate, win_rates_for_each_quarter, risk_to_reward_ratio, stoploss_hits, stoploss_misses, takeprofit_misses, average_number_of_consecutive_wins, average_number_of_consecutive_losses, maximum_number_of_consecutive_wins, number_of_times_the_maximum_number_of_consecutive_wins_occured, maximum_number_of_consecutive_losses, number_of_times_the_maximum_number_of_consecutive_losses_occured, maximum_waiting_time_without_a_trade_in_hours_and_minutes, average_waiting_time_without_a_trade_in_hours_and_minutes, minimum_waiting_time_without_a_trade_in_hours_and_minutes, number_of_features, training_data_start_date, training_data_end_date, training_data_number_of_trading_days, test_data_start_date, test_data_end_date, test_data_number_of_trading_days, predicted_actions_outcomes, win_lose_results, consecutive_wins, consecutive_losses, waiting_times_in_minutes, balances
    return maximum_trade_holding_time_in_hours_and_minutes, symbol, symbol_type, starting_account_balance, account_balance_after_trades, number_of_trades_taken, maximum_trade_holding_time_in_hours_and_minutes, trades_won, trades_lost, trades_still_open_on_training_completion, overall_win_rate, win_rates_for_each_quarter, risk_to_reward_ratio, stoploss_hits, stoploss_misses, takeprofit_misses, average_number_of_consecutive_wins, average_number_of_consecutive_losses, maximum_number_of_consecutive_wins, number_of_times_the_maximum_number_of_consecutive_wins_occured, maximum_number_of_consecutive_losses, number_of_times_the_maximum_number_of_consecutive_losses_occured, maximum_waiting_time_without_a_trade_in_hours_and_minutes, average_waiting_time_without_a_trade_in_hours_and_minutes, minimum_waiting_time_without_a_trade_in_hours_and_minutes, number_of_features, training_data_start_date, training_data_end_date, training_data_number_of_trading_days, test_data_start_date, test_data_end_date, test_data_number_of_trading_days, predicted_actions_outcomes, win_lose_results, consecutive_wins, consecutive_losses, waiting_times_in_minutes, balances
# *****************************************************************************************************************************************