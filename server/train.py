import os
from pandas import read_csv
from collections import deque
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from xgboost import XGBRegressor
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout, Bidirectional
from keras.callbacks import ModelCheckpoint
from keras.backend import clear_session
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import random
from pathlib import Path
import pickle
from settings import get_symbols, get_forecast_period, get_timeframes_in_use, training_data_source, prediction_data_source, use_closing_prices_only, get_training_logs_path, get_scalers_path, get_models_path, get_models_checkpoints_path, get_error_logs_path, scale_x, scale_y, x_use_percentages, y_use_percentages, index_of_model_to_use, show_plots_during_training, combine_training_and_validation_set, number_of_trees, shuffle_train_validation_data
from data import get_data

root = Path('.')

clear_session()

# ensure reproducibility in model training
seed = 42
random.seed(seed) # Python's built in random number generator
np.random.seed(seed) # NumPy's random number generator
tf.random.set_seed(seed) # TensorFlow's random number generator

def train(symbol):
    # timeframes in use
    timeframes = get_timeframes_in_use() # in descending order

    # get price data collection settings ... closing prices only / all ohlc prices
    closing_prices_only_status = use_closing_prices_only()

    # get dataframe / main dataset , x_column_list, y_column_1, and y_column_2
    dataframe, x_column_list, y_column_1, y_column_2 = get_data(
        symbol, # symbol for model being trained
        timeframes,  # timeframes in use
        training_data_source(), # where the data is supposed to come from
        'training', # purpose, what the data is being used for ... training / predicting ,
        closing_prices_only_status, # price data collection settings ... closing prices only / all ohlc prices
    )

    # create x and y dataframe
    x_dataframe = dataframe.filter(x_column_list)
    x_dataframe = x_dataframe.replace([np.inf, -np.inf], 0).fillna(0)
    y_dataframe = dataframe.filter([y_column_1, y_column_2])

    # get statistical description of y data
    y_dataframe_statistical_description = y_dataframe.describe()
    print('\n\nY Dataframe Statistical Description: \n', y_dataframe_statistical_description)

    # create numpy arrays of the data... x and y
    x = x_dataframe.values
    y = y_dataframe.values

    # test size
    test_size = 0.2

    # calculate split indices
    split_indices = int((1-test_size) * len(x))

    # create a test set that will be unseen from the model, either directly or via splits
    x_test = x[split_indices:]
    y_test = y[split_indices:]

    # get x and y without data used for the test set
    x = x[:split_indices]
    y = y[:split_indices]

    # print data shapes
    print('\n\nX Shape: ', x.shape)
    print('Y Shape: ', y.shape)
    print('X Test Shape: ', x_test.shape)
    print('Y Test Shape: ', y_test.shape, '\n\n')

    # split the data into train and validation sets ****************************
    validation_size = 0.2
    if shuffle_train_validation_data() == True:
        x_train, x_validation, y_train, y_validation = train_test_split(x, y, test_size=validation_size, shuffle=True, random_state=seed)
    else:
        # calculate split indices
        split_indices = int((1-validation_size) * len(x))
        # create splits
        x_train, x_validation = x[:split_indices], x[split_indices:]
        y_train, y_validation = y[:split_indices], y[split_indices:]

    # model to use
    models = ['LSTM', 'Random Forest', 'XGBoost', 'SVM', 'CNN'] # index of models to use will be referencing these
    index_of_model_to_use_ = index_of_model_to_use()

    # if set to true, combine training and validation sets into one training set ... for non keras models that cannot use a validation set during training
    if combine_training_and_validation_set() == True and index_of_model_to_use_ != 0 and index_of_model_to_use_ != 4:
        # combine x data
        x_train = np.concatenate((x_train, x_validation))

        # combine y data
        y_train = np.concatenate((y_train, y_validation))

    else:
        # print validation data shapes
        print('X Validation SHape: ', x_validation.shape)
        print('Y Validation Shape: ', y_validation.shape)

    # normalize x data sets
    if scale_x() == True:
        x_min_max_scaler = MinMaxScaler()
        x_scaler = x_min_max_scaler.fit(x_train)
        x_train = x_scaler.transform(x_train)
        x_validation = x_scaler.transform(x_validation)
        x_test = x_scaler.transform(x_test)

    # normalize y data sets
    if scale_y() == True:
        y_min_max_scaler = MinMaxScaler()
        y_scaler = y_min_max_scaler.fit(y_train)
        y_train = y_scaler.transform(y_train)
        y_validation = y_scaler.transform(y_validation)
        y_test = y_scaler.transform(y_test)

    # state features type inorder to retrieve model data accordingly ... C / OHLC
    if closing_prices_only_status == True:
        features_type = 'C'
    else:
        features_type = 'OHLC'

    # model checkpoint to save best weights encountered during training ... for models that can use checkpoints
    best_weights_filepath = get_models_checkpoints_path(symbol, timeframes, features_type)
    checkpoint = ModelCheckpoint(best_weights_filepath, monitor='val_mae', verbose=10, mode='min', save_best_only=True, save_weights_only=True)

    # train lstm
    if index_of_model_to_use_ == 0:
        # whether to use a bidirectional model or not
        use_bidirectional_model = False

        # reshape x data to give it the third dimension that will be the number of the single input rows as LSTM model input requires
        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
        x_validation = x_validation.reshape(x_validation.shape[0], x_validation.shape[1], 1)
        x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)
        print('x_train reshape: ', x_train.shape, '\n\n')
        print('x_validation reshape: ', x_validation.shape, '\n\n')
        print('x_test reshape: ', x_test.shape, '\n\n')

        # defining the input and output data dimensions from x and y data
        in_dim = (x_train.shape[1], x_train.shape[2])
        out_dim = y_train.shape[1]
        print('Input dimensions: ', in_dim, 'Output dimensions: ', out_dim, '\n\n')

        # whether to use dropout during training or not
        use_dropout = False

        # dropout value
        dropout = 0.1

        # number of neural networks
        number_of_neural_networks = 1

        # number of neural network nodes, for each network, [for network 1, for network 2, for network 3, etc...]
        neural_network_nodes = [200, 5, 5, 5, 5]

        # epochs
        epochs = 2000

        # batchsize
        batch_size = 1000

        # defining the model
        model = Sequential()
        for i in range(number_of_neural_networks):
            # network nodes
            network_nodes = neural_network_nodes[i]
            # return sequences
            if i == 0 and i != number_of_neural_networks - 1: # first lstm
                return_sequences = True
            if i == number_of_neural_networks - 1: # last lstm or when we only have one lstm
                return_sequences = False
            else: # mid lstms
                return_sequences = True
            # lstm
            if i == 0:
                if use_bidirectional_model == True:
                    model.add(Bidirectional(LSTM(network_nodes, input_shape=in_dim, activation="relu", return_sequences=return_sequences)))
                else:
                    model.add(LSTM(network_nodes, input_shape=in_dim, activation="relu", return_sequences=return_sequences))
            else:
                if use_bidirectional_model == True:
                    model.add(Bidirectional(LSTM(network_nodes, activation="relu", return_sequences=return_sequences)))
                else:
                    model.add(LSTM(network_nodes, activation="relu", return_sequences=return_sequences))
            # dropout
            if use_dropout == True:
                model.add(Dropout(dropout))
            # dense
            if i == number_of_neural_networks - 1:
                model.add(Dense(out_dim))

        # compile model ... Huberloss is tf.keras.losses.Huber() incase you'd want to use it
        model.compile(loss="mae", optimizer="adam", metrics=["mae"])

        # fitting the model with train data
        result = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=[checkpoint], verbose=2, validation_data=(x_validation, y_validation), shuffle=False)
        # print('\nResult history: ', result.history, '\n\n')
    
    # train random forest
    elif index_of_model_to_use_ == 1:
        # whether to use a bidirectional model or not ... stays False for this model
        use_bidirectional_model = False

        # n estimators
        n_estimators = number_of_trees()

        # random forest
        model = RandomForestRegressor(verbose=2, n_estimators=n_estimators, n_jobs=-1, random_state=seed)
        model.fit(x_train, y_train)

        # get random forest feature importance
        print('\n\nFeature importance (Random Forest):\n')
        importance = model.feature_importances_

        # summarize feature importance
        for i,v in enumerate(importance):
            # print('Feature: %0d, Score: %.5f' % (i,v))
            print('Feature name:', x_column_list[i], '| Score: ', v)
            
        # plot feature importance
        if show_plots_during_training() == True:
            plt.bar([x_column_list[x] for x in range(len(importance))], importance)
            plt.xticks(rotation=70, ha='right')
            plt.title("Random Forest Feature Importance")
            plt.xlabel("Features")
            plt.ylabel("Scores")
            plt.show()
            print('\n\n')

    # train xgboost
    elif index_of_model_to_use_ == 2:
        # whether to use a bidirectional model or not ... stays False for this model
        use_bidirectional_model = False

        # xgboost y column 1
        model_y_1 = XGBRegressor()
        model_y_1.fit(x_train, np.array([i[0] for i in y_train if True], dtype=float))

        # xgboost y column 2
        model_y_2 = XGBRegressor()
        model_y_2.fit(x_train, np.array([i[1] for i in y_train if True], dtype=float))

        # get gradient boost feature importance
        print('\n\nFeature importance (Gradient Boost Y1):\n')
        importance_y_1 = model_y_1.feature_importances_
        print('\n\nFeature importance (Gradient Boost Y2):\n')
        importance_y_2 = model_y_2.feature_importances_

        # summarize feature importance
        for i,v in enumerate(importance_y_1):
            # print('Feature: %0d, Score: %.5f' % (i,v))
            print('Feature name (Y1):', x_column_list[i], '| Score: ', v)
        for i,v in enumerate(importance_y_2):
            # print('Feature: %0d, Score: %.5f' % (i,v))
            print('Feature name (Y2):', x_column_list[i], '| Score: ', v)

        # plot feature importance
        if show_plots_during_training() == True:
            plt.bar([x_column_list[x] for x in range(len(importance_y_1))], importance_y_1)
            plt.xticks(rotation=70, ha='right')
            plt.title("Gradient Boost Feature Importance (Y1)")
            plt.xlabel("Features")
            plt.ylabel("Scores")
            plt.show()
            print('\n\n')
        if show_plots_during_training() == True:
            plt.bar([x_column_list[x] for x in range(len(importance_y_2))], importance_y_2)
            plt.xticks(rotation=70, ha='right')
            plt.title("Gradient Boost Feature Importance (Y2)")
            plt.xlabel("Features")
            plt.ylabel("Scores")
            plt.show()
            print('\n\n')

    # train svm
    elif index_of_model_to_use_ == 3:
        # whether to use a bidirectional model or not ... stays False for this model
        use_bidirectional_model = False

        # svm y column 1
        model_y_1 = SVR(verbose=True)
        model_y_1.fit(x_train, np.array([i[0] for i in y_train if True], dtype=float))

        # svm y column 2
        model_y_2 = SVR(verbose=True)
        model_y_2.fit(x_train, np.array([i[1] for i in y_train if True], dtype=float))

    # train cnn
    elif index_of_model_to_use_ == 4:
        # whether to use a bidirectional model or not ... stays False for this model
        use_bidirectional_model = False

        # reshape x data to give it the third dimension that will be the number of the single input rows as LSTM model input requires
        x_train = x_train.reshape(x_train.shape[0], x_train.shape[1], 1)
        x_validation = x_validation.reshape(x_validation.shape[0], x_validation.shape[1], 1)
        x_test = x_test.reshape(x_test.shape[0], x_test.shape[1], 1)
        print('x_train reshape: ', x_train.shape, '\n\n')
        print('x_validation reshape: ', x_validation.shape, '\n\n')
        print('x_test reshape: ', x_test.shape, '\n\n')

        # epochs
        epochs = 100

        # batchsize
        batch_size = 64

        # define CNN model
        model = keras.Sequential([
            layers.Conv1D(filters=32, kernel_size=3, activation="relu", input_shape=(x_train.shape[1], x_train.shape[2])),
            layers.MaxPooling1D(pool_size=2),
            layers.Flatten(),
            layers.Dense(16, activation="relu"),
            layers.Dense(2)  # Output layer for price prediction
        ])

        # compile the model ...  Huberloss is tf.keras.losses.Huber() incase you'd want to use it
        model.compile(loss="mae", optimizer="adam", metrics=["mae"])  

        # train the model on your data (split into training and validation sets)
        result = model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=[checkpoint], verbose=2, validation_data=(x_validation, y_validation), shuffle=False)

    # unknown model index
    else:
        print('\n\nUnknown Model Index Selected!')
        quit()

    # for keras models ... plot training history 
    if index_of_model_to_use_ == 0 or index_of_model_to_use_ == 4:
        # get the best validation mae of the training epochs
        best_validation_mae = np.amin(result.history['val_mae']) 
        print('Best validation mae encountered during epochs:', best_validation_mae)

        # plot history
        if show_plots_during_training() == True:
            plt.plot(result.history['loss'], label='Training Loss')
            plt.plot(result.history['mae'], label='Taining MAE')
            plt.plot(result.history['val_loss'], label='Validation Loss')
            plt.plot(result.history['val_mae'], label='Validation MAE')
            plt.legend()
            plt.show()
            
        # load best weights to model
        model.load_weights(best_weights_filepath)

    # ..................................................evaluate trained model .........................................
    # evaluate validation set ... for non keras models *******************************************
    if combine_training_and_validation_set() == False and index_of_model_to_use_ != 0 and index_of_model_to_use_ != 4:
        # make predictions using the validation set
        if index_of_model_to_use_ == 2 or index_of_model_to_use_ == 3: # models that do one output at a time
            y_column_1_predicted = model_y_1.predict(x_validation)
            y_column_2_predicted = model_y_2.predict(x_validation)

            # join predictions to form one y predicted
            y_validation_predicted = np.array([np.array([i, j], dtype=float) for i, j in zip(y_column_1_predicted, y_column_2_predicted) if True], dtype=float)

        else: # models that can do multiple outputs at a time
            y_validation_predicted = model.predict(x_validation)

        # y inversion to original scale
        if scale_y() == True:
            # invert actual y validation to original scale
            y_validation = y_scaler.inverse_transform(y_validation)

            # invert predicted y validation to original y scale
            y_validation_predicted = y_scaler.inverse_transform(y_validation_predicted)

        # calculate validation set mse
        validation_mse = mean_squared_error(y_validation, y_validation_predicted)
        print('\n\nValidation MSE:', validation_mse)

        # calculate validation set rmse
        validation_rmse = np.sqrt(validation_mse)
        print('Validation RMSE:', validation_rmse)

        # calculate validation set mae
        validation_mae = mean_absolute_error(y_validation, y_validation_predicted)
        print('Validation MAE:', validation_mae, '\n\n')

    # make predictions using the test set ********************************************************************
    if index_of_model_to_use_ == 2 or index_of_model_to_use_ == 3: # models that do one output at a time
        y_column_1_predicted = model_y_1.predict(x_test)
        y_column_2_predicted = model_y_2.predict(x_test)

        # join predictions to form one y predicted
        y_predicted = np.array([np.array([i, j], dtype=float) for i, j in zip(y_column_1_predicted, y_column_2_predicted) if True], dtype=float)

    else: # models that can do multiple outputs at a time
        y_predicted = model.predict(x_test)

    # y inversion to original scale
    if scale_y() == True:
        # invert y actual to original scale
        y_test = y_scaler.inverse_transform(y_test)

        # invert y predicted to original y scale
        y_predicted = y_scaler.inverse_transform(y_predicted)

    # calculate test set mse
    mse = mean_squared_error(y_test, y_predicted)
    print('\n\nTest MSE:', mse)

    # calculate test set rmse
    rmse = np.sqrt(mse)
    print('Test RMSE:', rmse)

    # calculate test set mae
    mae = mean_absolute_error(y_test, y_predicted)
    print('Test MAE:', mae, '\n\n')

    # get lists of actual values and predicted values for each column
    actual_max_down = np.array([i[0] for i in y_test if True], dtype=float)
    actual_max_up = np.array([i[1] for i in y_test if True], dtype=float)
    predicted_max_down = np.array([i[0] for i in y_predicted if True], dtype=float)
    predicted_max_up = np.array([i[1] for i in y_predicted if True], dtype=float)

    # plot predicted vs actual
    if show_plots_during_training() == True:
        plt.plot(actual_max_down, label='Actual Max Down')
        plt.plot(actual_max_up, label='Actual Max Up')
        plt.plot(predicted_max_down, label='Predicted Max Down')
        plt.plot(predicted_max_up, label='Predicted Max Up')
        plt.title('Predicted vs Actual')
        plt.legend()
        plt.show()

    # get lists of differences between actual values and predicted values 
    max_down_differences = np.array([abs(i[0] - j[0]) for i, j in zip(y_test, y_predicted) if True], dtype=float)
    max_up_differences = np.array([abs(i[1] - j[1]) for i, j in zip(y_test, y_predicted) if True], dtype=float)

    # plot differences between actual values and predicted values ... plot mae and rmse horizontal lines as well for comparisons
    if show_plots_during_training() == True:
        plt.plot(np.array([mae for i in range(len(max_down_differences))], dtype=float), label='Mean Absolute Error (MAE)')
        plt.plot(np.array([rmse for i in range(len(max_down_differences))], dtype=float), label='Root Mean Squared Error (RMSE)')
        plt.plot(max_down_differences, label='Max Down Differences')
        plt.plot(max_up_differences, label='Max Up Differences')
        plt.title('Differences between Predicted and Actual')
        plt.legend()
        plt.show()

    # # plotting difference as percentages if we're using price features and not percentage ones 
    # if x_use_percentages() == False and use_weighted_features() == False:
    #     # get lists of differences between actual values and predicted values as percentages
    #     max_down_differences_percentages = np.array([abs(i[0] - j[0]) for i, j in zip(y_test, y_predicted) if True], dtype=float)
    #     max_up_differences_percentages = np.array([abs(i[1] - j[1]) for i, j in zip(y_test, y_predicted) if True], dtype=float)

    #     # plot percentage differences between actual values and predicted values 
    #     if show_plots_during_training() == True:
    #         plt.plot(max_down_differences_percentages, label='Max Down Differences (Percentage)')
    #         plt.plot(max_up_differences_percentages, label='Max Up Differences (Percentage)')
    #         plt.title('Percentage Differences between Predicted and Actual')
    #         plt.legend()
    #         plt.show()

    # state features type inorder to save model data accordingly ... C / OHLC
    if closing_prices_only_status == True:
        features_type = 'C'
    else:
        features_type = 'OHLC'

    # state model type Bidirectional / Undirectional
    if use_bidirectional_model == True:
        model_type = 'Bidirectional'
    else:
        model_type = 'Undirectional'

    # save training logs to a file
    training_logs_path = get_training_logs_path(symbol, timeframes, features_type)
    if index_of_model_to_use_ == 0: # lstm
        training_log = """
Index of Model: {index_of_model_to_use_}

Use Droput: {use_dropout}

Dropout: {dropout}

Number of Neural Networks: {number_of_neural_networks}

Neural Network Nodes: {neural_network_nodes}

Epochs: {epochs}

Batchsize: {batch_size}

Input Dimensions: {in_dim}

Output Dimensions: {out_dim}

X Validation Shape = {x_validation_shape}

Y Validation Shape = {y_validation_shape}

Best Validation MAE = {best_validation_mae}

        """.format(
            index_of_model_to_use_ = index_of_model_to_use_,
            use_dropout = use_dropout, dropout = dropout, number_of_neural_networks = number_of_neural_networks, 
            neural_network_nodes = neural_network_nodes, epochs = epochs, batch_size = batch_size, 
            in_dim = in_dim, out_dim = out_dim, best_validation_mae = best_validation_mae, 
            x_validation_shape = x_validation.shape, y_validation_shape = y_validation.shape
        )

    elif index_of_model_to_use_ == 1: # random forest
        training_log = """
Index of Model: {index_of_model_to_use_}

N Estimators: {n_estimators}

        """.format(
            index_of_model_to_use_ = index_of_model_to_use_, n_estimators = n_estimators
        )

    elif index_of_model_to_use_ == 2: # xgboost
        training_log = """
Index of Model: {index_of_model_to_use_}

        """.format(
            index_of_model_to_use_ = index_of_model_to_use_
        )

    elif index_of_model_to_use_ == 3: # svm
        training_log = """
Index of Model: {index_of_model_to_use_}

        """.format(
            index_of_model_to_use_ = index_of_model_to_use_
        )
    
    elif index_of_model_to_use_ == 4: # cnn
        training_log = """
Index of Model: {index_of_model_to_use_}

        """.format(
            index_of_model_to_use_ = index_of_model_to_use_
        )

    # compile training log
    training_log = training_log + """
Timeframes: {timeframes_}

Model Type: {model_type}

Y Dataframe Statistical Description: {y_dataframe_statistical_description}

X Shape: {x_shape}

Y Shape: {y_shape}

X Train Shape: {x_train_shape}

X Test Shape: {x_test_shape}

X Use Percentages: {x_use_percentages_}

Y Use Percentages: {y_use_percentages_}

Scale X: {scale_x_}

Scale Y: {scale_y_}

Test MSE: {mse}

Test RMSE: {rmse}

Test MAE: {mae}

Actual Max Down Values: {actual_max_down}

Predicted Max Down Values: {predicted_max_down}

Max Down Differences: {max_down_differences}

Actual Max Up Values: {actual_max_up}

Predicted Max Up Values: {predicted_max_up}

Max Up Differences: {max_up_differences}

    """.format(
        model_type = model_type, scale_x_ = scale_x(), scale_y_ = scale_y(), x_use_percentages_ = x_use_percentages(), y_use_percentages_ = y_use_percentages(),
        mse = mse, rmse = rmse, mae = mae,  
        y_dataframe_statistical_description = y_dataframe_statistical_description, x_shape = x.shape, y_shape = y.shape, 
        x_train_shape = x_train.shape, x_test_shape = x_test.shape, 
        timeframes_ = str(timeframes),
        actual_max_down = actual_max_down, actual_max_up = actual_max_up, predicted_max_down = predicted_max_down, predicted_max_up = predicted_max_up,
        max_down_differences = max_down_differences, max_up_differences = max_up_differences
    )
    # add result history ... keras models
    if index_of_model_to_use_ == 0 or index_of_model_to_use_ == 4:
        training_log = training_log + """
Result History: {result_history}
        """.format(result_history = result.history)

    # add validation set ... for non keras models
    if combine_training_and_validation_set() == False and index_of_model_to_use_ != 0 and index_of_model_to_use_ != 4:
        training_log = training_log + """
X Validation Shape: {x_validation_shape}

Y Validation Shape: {y_validation_shape}

Validation MSE: {validation_mse}

Validation RMSE: {validation_rmse}

Validation MAE: {validation_mae}
        """.format(
            x_validation_shape = x_validation.shape, y_validation_shape = y_validation.shape,
            validation_mse = validation_mse, validation_rmse = validation_rmse, validation_mae = validation_mae
        )

    # save training logs
    with open(training_logs_path, 'w') as file:
        file.write(training_log)

    ######################################
    # quit()

    # save and encrypt x scaler ******************
    if scale_x() == True:
        # x scaler path
        x_scaler_path = get_scalers_path(symbol, timeframes, features_type, 'x')
        # serialize x scaler, using pickle
        pickle_x_scaler = pickle.dumps(x_scaler)
        # save x scaler to a file
        with open(x_scaler_path, 'wb') as file:
            file.write(pickle_x_scaler)

    # save and encrypt y scaler *******************
    if scale_y() == True:
        # y scaler path
        y_scaler_path = get_scalers_path(symbol, timeframes, features_type, 'y')
        # serialize y scaler, using pickle
        pickle_y_scaler = pickle.dumps(y_scaler)
        # save y scaler to a file
        with open(y_scaler_path, 'wb') as file:
            file.write(pickle_y_scaler)

    # save and encrypt model ***********************
    if index_of_model_to_use_ == 2 or index_of_model_to_use_ == 3: # models that do one output at a time
        # model paths
        model_path_y_1, model_path_y_2  = get_models_path(symbol, timeframes, features_type)
        # serialize models, using pickle
        pickle_model_y_1 = pickle.dumps(model_y_1)
        pickle_model_y_2 = pickle.dumps(model_y_2)
        # save models to files
        with open(model_path_y_1, 'wb') as file:
            file.write(pickle_model_y_1)
        with open(model_path_y_2, 'wb') as file:
            file.write(pickle_model_y_2)

    else: # models that can do multiple outputs at a time
        # model path
        model_path = get_models_path(symbol, timeframes, features_type)
        # serialize model, using pickle
        pickle_model = pickle.dumps(model)
        # encrypt model
        encrypted_model = cipher_suite.encrypt(pickle_model)
        # save model to a file
        with open(model_path, 'wb') as file:
            file.write(encrypted_model)

    print(symbol, model_type, 'Model training complete')

# get list of symbols
symbols = get_symbols()

# train models for each symbol
for symbol in symbols:
    print('\n\nTraining', symbol, 'Model............................................')
    train(symbol)