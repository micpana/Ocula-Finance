from symbol_config import get_symbol_list, get_symbol_config
from models import MarketAnalysis
from database import init_db
from pytz import timezone
from datetime import datetime, timedelta, date
from settings import save_live_predictions_to_database, print_live_predictions_to_console
from y_feature_engineering import engineer_y

# initialize database connection in this module *******************************************************************************************
# proceed if the database is being used during predictions
if save_live_predictions_to_database() == True:
    init_db()
# *****************************************************************************************************************************************

# get list of symbols *********************************************************************************************************************
list_of_symbols = get_symbol_list()
# printout the list of symbols being used
print('\n\nManaging trades for the following symbols:', list_of_symbols)
# *****************************************************************************************************************************************

# function for managing open trades *******************************************************************************************************
def manage_open_trades(symbols_engineered_x_datasets_dict, entry_timeframe):
    # get current datetime object ... in format: yyyy-mm-dd hh:mm
    date_format = '%Y-%m-%d %H:%M'
    current_datetime = datetime.now(timezone(system_timezone())).strftime(date_format)
    current_datetime_object = datetime.strptime(current_datetime, date_format)

    # loop through symbols ******************************************************************************************************
    for symbol in list_of_symbols:
        # check if symbol has open trades *****************************************************************************
        # get symbol's trades whose expiry hasn't been managed yet
        trades_with_unmanaged_expiry = MarketAnalysis.objects.filter(symbol = symbol, expiry_already_managed_by_system = False)

        # get unmanaged trades whose maximum holding time has already been reached
        expired_trades_with_unmanaged_expiry = [trade for trade in trades_with_unmanaged_expiry if str(current_datetime_object) >= trade.maximum_holding_time_timestamp]
        # *************************************************************************************************************

        # if we do have unmanaged trades whose maximum holding time has already been reached **************************
        if len(expired_trades_with_unmanaged_expiry) > 0:
            # signal the management of the current symbol's open trades
            print('Managing Found ', symbol, 'Expired Trade(s)...\n\n')

            # get symbol data *******************************************************************************
            # get symbol config
            symbol_config = get_symbol_config(symbol)

            # reward ... minimum buy or sell target percentage
            reward = symbol_config['target']

            # risk target divisor
            risk_target_divisor = symbol_config['risk_target_divisor']

            # risk ... stoploss
            risk = reward / risk_target_divisor

            # risk:reward
            risk_to_reward_ratio = '1:'+str(risk_target_divisor)
            
            # forecast period
            forecast_period = symbol_config['forecast_period']
            # ***********************************************************************************************

            # get x features dataframe **********************************************************************
            x_features_dataframe = symbols_engineered_x_datasets_dict[symbol]
            # ***********************************************************************************************

            # get y features dataframe **********************************************************************
            y_features_dataframe = engineer_y(x_features_dataframe, y_type, entry_timeframe, symbol)
            # ***********************************************************************************************

            # get required numpy arrays from x and y features dataframes, minus last n (forecast_period)*****
            # entry timeframe timestamps
            timestamps = np.array(x_features_dataframe[entry_timeframe+'_Timestamp'].values[:-forecast_period], dtype=str)
            # entry timeframe opens
            opens = x_features_dataframe[entry_timeframe+'_Open'].values[:-forecast_period]
            # entry timeframe highs
            highs = x_features_dataframe[entry_timeframe+'_High'].values[:-forecast_period]
            # entry timeframe lows
            lows = x_features_dataframe[entry_timeframe+'_Low'].values[:-forecast_period]
            # entry timeframe closes
            closes = x_features_dataframe[entry_timeframe+'_Close'].values[:-forecast_period]
            # maximum percentages up
            maximum_percentages_up = y_features_dataframe['Max % Up'].values[:-forecast_period]
            # maximum percentages down
            maximum_percentages_down = y_features_dataframe['Max % Down'].values[:-forecast_period]
            # trade's session closing percentages
            trade_session_closing_percentages = y_features_dataframe["Trade's Session Closing %"].values[:-forecast_period]
            # ***********************************************************************************************

            # loop through expired_trades_with_unmanaged_expiry *********************************************
            for trade in expired_trades_with_unmanaged_expiry:
                # trade's entry timeframe timestamp
                trade_entry_timeframe_timestamp = trade.entry_timeframe_timestamp

                # trade's action
                trade_action = trade.predicted_trading_action

                # find trade's index in timestamps array from our engineered data *****************
                # trade index array
                trade_index_array = np.where(timestamps == trade_entry_timeframe_timestamp)[0]
                # if trade index array has contents
                if len(trade_index_array) > 0:
                    # get trade index
                    trade_index = trade_index_array[0]

                    # get trade's maximum percentage up
                    trade_maximum_percentage_up = maximum_percentages_up[trade_index]

                    # get trade's maximum percentage down
                    trade_maximum_percentage_down = maximum_percentages_down[trade_index]

                    # get trade's session closing percentage
                    trade_session_closing_percentage = trade_closing_percentages[trade_index]

                    # check if trade was a win or lose **********************************
                    # if trade was a buy
                    if trade_action == 'Buy':
                        # check if takeprofit was hit
                        if trade_maximum_percentage_up >= reward:
                            # set takeprofit hit to true
                            takeprofit_hit = True
                            # set stoploss hit to false
                            stoploss_hit = False
                            # set trade closing percentage
                            trade_close_percentage = reward
                            # set trade won to true
                            trade_won = True
                        # check if stoploss was hit
                        elif trade_maximum_percentage_down <= -risk:
                            # set takeprofit hit to false
                            takeprofit_hit = False
                            # set stoploss hit to true
                            stoploss_hit = True
                            # set trade closing percentage
                            trade_close_percentage = -risk
                            # set trade won to false
                            trade_won = False
                        # if both takeprofit and stoploss were not hit
                        else:
                            # set takeprofit hit to false
                            takeprofit_hit = False
                            # set stoploss hit to false
                            stoploss_hit = False
                            # set trade closing percentage
                            trade_close_percentage = trade_session_closing_percentage
                            # set trade won to false
                            trade_won = False

                    # if trade was a sell
                    elif trade_action == 'Sell':
                        # check if takeprofit was hit
                        if trade_maximum_percentage_down <= -reward:
                            # set takeprofit hit to true
                            takeprofit_hit = True
                            # set stoploss hit to false
                            stoploss_hit = False
                            # set trade closing percentage
                            trade_close_percentage = -reward
                            # set trade won to true
                            trade_won = True
                        # check if stoploss was hit
                        elif trade_maximum_percentage_up >= risk:
                            # set takeprofit hit to false
                            takeprofit_hit = False
                            # set stoploss hit to true
                            stoploss_hit = True
                            # set trade closing percentage
                            trade_close_percentage = risk
                            # set trade won to false
                            trade_won = False
                        # if both takeprofit and stoploss were not hit
                        else:
                            # set takeprofit hit to false
                            takeprofit_hit = False
                            # set stoploss hit to false
                            stoploss_hit = False
                            # set trade closing percentage
                            trade_close_percentage = trade_session_closing_percentage
                            # set trade won to false
                            trade_won = False
                    # *******************************************************************

                    # update trade's information in the database ************************
                    MarketAnalysis.objects(id = str(trade.id)).update(
                        expiry_already_managed_by_system = True,
                        stoploss_hit = stoploss_hit,
                        takeprofit_hit = takeprofit_hit,
                        trade_close_percentage = trade_close_percentage,
                        trade_won = trade_won
                    )
                    # *******************************************************************

                    # if predictions are being printed to the console *******************
                    # if print_live_predictions_to_console() == True:
                        
                    # *******************************************************************
                # *********************************************************************************
            # ***********************************************************************************************
        # *************************************************************************************************************
    # ***************************************************************************************************************************
# *****************************************************************************************************************************************