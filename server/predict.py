import pickle
import numpy as np
from settings import get_symbols, get_forecast_period, get_timeframes_in_use, training_data_source, prediction_data_source, use_closing_prices_only, get_training_logs_path, get_scalers_path, get_models_path, get_models_checkpoints_path, get_error_logs_path, system_timezone, run_predictions_as_flask_thread, scale_x, scale_y, index_of_model_to_use, save_live_predictions_to_database, print_live_predictions_to_console
from pytz import timezone
from datetime import datetime, timedelta, date
from data import get_data

# if predictions are being saved to the database
if save_live_predictions_to_database() == True:
    # db related imports
    from models import MarketAnalysis
    from database import init_db
    # initialize module's connection to the db
    init_db()

# prediction_key variable will come from decryption file, its being used in this file but it will not be declared or imported into this file

# cipher suite ... Fernet not to be imported or declared into this file, it will come from decryption file
cipher_suite = Fernet(prediction_key)

# make predictions
def predict(symbol):
    # timeframes in use
    timeframes = get_timeframes_in_use() # in descending order

    # get price data collection settings ... closing prices only / all ohlc prices
    closing_prices_only_status = use_closing_prices_only()

    # get input dataframe
    dataframe, entry_timeframe_last_datetime = get_data(
        symbol, # symbol for model being trained
        timeframes,  # timeframes in use
        prediction_data_source(), # where the data is supposed to come from
        'predicting', # purpose, what the data is being used for ... training / predicting ,
        closing_prices_only_status, # price data collection settings ... closing prices only / all ohlc prices
    )

    # check if prediction data is new or a prediction for this data has already been done ... check using entry timeframe's last datetime
    entry_timeframe_datetime_already_used = False
    if save_live_predictions_to_database() == True
        if len(MarketAnalysis.objects.filter(symbol = symbol, entry_timeframe_last_timestamp = entry_timeframe_last_datetime)) > 0:
            entry_timeframe_datetime_already_used = True

    # if data has not been used for a prediction saved within our database, proceed to make a prediction
    if entry_timeframe_datetime_already_used == False:
        # get last dataframe row
        x_input = dataframe.iloc[[len(dataframe) - 1]]

        # reset x_input indexes
        x_input.reset_index(drop=True, inplace=True)

        # create numpy arrays of the data ... x
        x = x_input.values

        # state features type inorder to retrieve model data accordingly ... C / OHLC
        if closing_prices_only_status == True:
            features_type = 'C'
        else:
            features_type = 'OHLC'

        # scale x data **********************
        if scale_x() == True:
            x_scaler_path = get_scalers_path(symbol, timeframes, features_type, 'x')
            # decrypt x scaler file
            with open(x_scaler_path, 'rb') as file:
                x_scaler = pickle.loads(cipher_suite.decrypt(file.read()))
            x = x_scaler.transform(x)

        # model to use ... names listed in training module
        index_of_model_to_use_ = index_of_model_to_use()

        # reshape x data to give it the third dimension that will be the number of the single input rows as LSTM model input requires
        if index_of_model_to_use_ == 0:
            x = x.reshape(x.shape[0], x.shape[1], 1)

        # predict *************************
        if index_of_model_to_use_ == 2 or index_of_model_to_use_ == 3: # models that do one output at a time
            # model paths
            model_path_y_1, model_path_y_2 = get_models_path(symbol, timeframes, features_type)
            # decrypt model files
            with open(model_path_y_1, 'rb') as file:
                model_y_1 = pickle.loads(cipher_suite.decrypt(file.read()))
            with open(model_path_y_2, 'rb') as file:
                model_y_2 = pickle.loads(cipher_suite.decrypt(file.read()))
            # predict
            prediction_y_1 = model_y_1.predict(x)
            prediction_y_2 = model_y_2.predict(x)
            # join predictions to form one predictions variable
            predictions = np.array([np.array([i, j], dtype=float) for i, j in zip(prediction_y_1, prediction_y_2) if True], dtype=float)

        else: # models that can do multiple outputs at a time
            # model path
            model_path = get_models_path(symbol, timeframes, features_type)
            # decrypt model file
            with open(model_path, 'rb') as file:
                model = pickle.loads(cipher_suite.decrypt(file.read()))
            # predict
            predictions = model.predict(x)

        # invert the predicted data's scale ***********************
        if scale_y() == True:
            y_scaler_path = get_scalers_path(symbol, timeframes, features_type, 'y')
            # decrypt y scaler file
            with open(y_scaler_path, 'rb') as file:
                y_scaler = pickle.loads(cipher_suite.decrypt(file.read()))
            predictions = y_scaler.inverse_transform(predictions)

        # get predicted values as standalone variables
        predictions = predictions[0]
        maximum_possible_down_move = predictions[0]
        maximum_possible_up_move = predictions[1]

        # if predictions are being saved to the database
        if save_live_predictions_to_database() == True:
            # save predictions to database 
            prediction_details = MarketAnalysis(
                timestamp = str(datetime.now(timezone(system_timezone()))),
                entry_timeframe_last_timestamp = entry_timeframe_last_datetime,
                asset = symbol,
                maximum_possible_down_move = maximum_possible_down_move,
                maximum_possible_up_move = maximum_possible_up_move
            )
            prediction_details.save()

        # if predictions are being printed to the console
        if print_live_predictions_to_console() == True:
            # print prediction data
            print('\n\n', symbol, '---> Max Down:', maximum_possible_down_move, 'Max Up:', maximum_possible_up_move, 'Time:', str(datetime.now(timezone(system_timezone()))))
    
    else: # data has already been used
        print('\n\nCurrent', symbol, 'data has already been used to make a prediction which is present in our database. Will make a new prediction when new data is received')

# run predictions
def run_predictions():
    # get list of symbols
    symbols = get_symbols()

    # mark last prediction run
    last_prediction_run_datetime_object = None

    # indicate that the prediction module is now running
    print('Prediction module running (for ' + str(symbols) + ' )...')

    # continuous prediction loop
    while True:
        # get current day
        current_day = date.today().isoweekday()

        # check if its a weekday ... 1 is Monday, 5 is Friday
        if (current_day >= 1) and (current_day <= 5):
            # list of minutes to perform predictions ... every 15 minutes as per M15 candle close
            minutes = ['00', '15', '30', '45']

            # get current datetime object ... in format: yyyy-mm-dd hh:mm
            date_format = '%Y-%m-%d %H:%M'
            current_datetime = datetime.now().strftime(date_format)
            current_datetime_object = datetime.strptime(current_datetime, date_format)

            # get current minute
            current_minute = str(current_datetime_object.minute)

            # make predictions for each symbol ... on every 15th minute, ie, :00, :15, :30, :45
            if current_minute in minutes:
                # check if this is a new prediction run
                if last_prediction_run_datetime_object != current_datetime_object:
                    # perform predictions
                    for symbol in symbols:
                        print('Running predictions for', symbol)
                        predict(symbol)
                        
                    # mark prediction run as latest
                    last_prediction_run_datetime_object = current_datetime_object

# run
if run_predictions_as_flask_thread() == False:
    run_predictions()
else:
    print('Predictions set to run as flask thread. If you intent to run predictions outside of the main flask app, change the settings.')