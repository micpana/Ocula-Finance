from collections import deque
from symbol_config import get_symbol_list, get_symbol_config
from settings import predictions_filter_config

# filtering predictions using a probability threshold *************************************************************************************
filter_predictions_using_a_probability_threshold, prediction_probability_threshold = predictions_filter_config()
# *****************************************************************************************************************************************

# get trade outcome ***********************************************************************************************************************
def get_trade_outcome(symbol, trade_action, trade_maximum_percentage_up, trade_maximum_percentage_down, trade_session_closing_percentage):
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

    # symbol type
    symbol_type = symbol_config['type']
    # ***************************************************************************************************************************

    # check if trade was a win or lose ******************************************************************************************
    # if trade was a buy
    if trade_action == 'Buy':
        # if takeprofit was hit
        if trade_maximum_percentage_up >= reward: takeprofit_hit = True; stoploss_hit = False; trade_close_percentage = reward; trade_won = True
        # if stoploss was hit
        elif trade_maximum_percentage_down <= -risk: takeprofit_hit = False; stoploss_hit = True; trade_close_percentage = -risk; trade_won = False
    
    # if trade was a sell
    elif trade_action == 'Sell':
        # if takeprofit was hit
        if trade_maximum_percentage_down <= -reward: takeprofit_hit = True; stoploss_hit = False; trade_close_percentage = -reward; trade_won = True
        # check if stoploss was hit
        elif trade_maximum_percentage_up >= risk: takeprofit_hit = False; stoploss_hit = True; trade_close_percentage = risk; trade_won = False
        
    # if both takeprofit and stoploss were not hit
    if (trade_action == 'Buy' or trade_action == 'Sell') and (takeprofit_hit != True and stoploss_hit != True):
        takeprofit_hit = False; stoploss_hit = False; trade_close_percentage = trade_session_closing_percentage; trade_won = False
    # ***************************************************************************************************************************

    # return takeprofit_hit, stoploss_hit, trade_close_percentage, trade_won
    return takeprofit_hit, stoploss_hit, trade_close_percentage, trade_won
# *****************************************************************************************************************************************

# get trade outcomes **********************************************************************************************************************
def get_trade_outcomes(symbol, y_test, y_predicted, y_predicted_probabilities):
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

    # symbol type
    symbol_type = symbol_config['type']
    # ***************************************************************************************************************************

    # get insights on the predicted trades **************************************************************************************
    # state risk amount ... eg risking a dollar on each trade
    risk_amount = 1 # dollar(s)
    # state initial account balance
    initial_balance = 100 # dollar(s)
    # initialize current account balance ... to get a equity graph using the predicted trades
    current_balance = initial_balance
    # initialize array store current balances
    current_balances = deque([])
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
    takeprofits = deque([])
    # initialize array to store stoplosses for predicted trades
    stoplosses = deque([])
    # initialize array to store stoploss hit statuses
    stoploss_hit_statuses = deque([])
    # initialize array to store stoploss missed statuses
    stoploss_missed_statuses = deque([])
    # initialize array to store takeprofit missed statuses
    takeprofit_missed_statuses = deque([])
    # compare actual vs predicted and get wanted win / lose results ***************************************************
    for i in tqdm(range(len(y_test)), desc="Predicted Trades Insight Generation", unit="row"):
        # get actual value and predicted value, plus the predicted probabilities, and the max predicted probability (max predicted probability is the probability of the predicted class)
        actual = y_test[i]; predicted = y_predicted[i]; predicted_probabilities = y_predicted_probabilities[i]; max_predicted_probability = np.max(predicted_probabilities)
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
                # takeprofit
                takeprofit = predicted_buy_price + ((reward / 100) * predicted_buy_price)
                # stoploss
                stoploss = predicted_buy_price - ((risk / 100) * predicted_buy_price)
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
                # takeprofit
                takeprofit = predicted_sell_price - ((reward / 100) * predicted_sell_price)
                # stoploss
                stoploss = predicted_sell_price + ((risk / 100) * predicted_sell_price)
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
        # append current balance ******************************************************************
        current_balances.append(current_balance)
        # *****************************************************************************************
        # append actions to their respective arrays ***********************************************
        predicted_buy_prices.append(predicted_buy_price)
        predicted_sell_prices.append(predicted_sell_price)
        # *****************************************************************************************
        # append takeprofits and stoplosses to their respective arrays ****************************
        takeprofits.append(takeprofit)
        stoplosses.append(stoploss)
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
    waiting_times_in_minutes = np.array(waiting_times_in_minutes)
    # ***************************************************************************************************************************

    # return current_balances, win_lose_results, consecutive_wins, consecutive_losses, predicted_buy_prices, predicted_sell_prices, takeprofits, stoplosses, stoploss_hit_statuses, stoploss_missed_statuses, takeprofit_missed_statuses, waiting_times_in_minutes
    return current_balances, win_lose_results, consecutive_wins, consecutive_losses, predicted_buy_prices, predicted_sell_prices, takeprofits, stoplosses, stoploss_hit_statuses, stoploss_missed_statuses, takeprofit_missed_statuses, waiting_times_in_minutes
# *****************************************************************************************************************************************

#