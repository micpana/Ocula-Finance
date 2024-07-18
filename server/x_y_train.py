from x_y_feature_engineering import engineer_x_y
from sklearn.preprocessing import MinMaxScaler
import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from imblearn.ensemble import BalancedRandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import pandas as pd
import collections
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder

# ensure reproducibility ******************************************************************************************************************
seed = 42
random.seed(seed) # Python's built in random number generator
np.random.seed(seed) # NumPy's random number generator
# *****************************************************************************************************************************************

# symbol
symbol = 'EURUSD'

# y type
y_type = 'buy or sell'  # buy or sell / minimum maximum

# get feature engineered dataset
dataset, x_column_list, y_column_list = engineer_x_y(symbol, y_type)

# delete entry timeframe timestamp column
del dataset['M15_Timestamp']

# test size
test_size = 0.2

# test dataset length
test_dataset_length = int(test_size * len(dataset))

# train dataset length
train_dataset_length = int(len(dataset) - test_dataset_length)

# split dataset into train and test
train_dataset = dataset.head(train_dataset_length)
test_dataset =  dataset.tail(test_dataset_length)

# shuffle train dataset
train_dataset = train_dataset.sample(frac=1.0)

# initialize label encoder ... to encode string labels to numerical labels ... xgbclassifier requirement for the target variable
label_encoder = LabelEncoder()

# get our train and test sets
x_train = train_dataset.filter(x_column_list).values
y_train = label_encoder.fit_transform(train_dataset.filter(y_column_list).values)
x_test = test_dataset.filter(x_column_list).values
y_test = label_encoder.fit_transform(test_dataset.filter(y_column_list).values)

# print data shapes
print('\n\nX Train Shape: ', x_train.shape)
print('Y Train Shape: ', y_train.shape)
print('X Test Shape: ', x_test.shape)
print('Y Test Shape: ', y_test.shape, '\n\n')

# scale x data
min_max_scaler = MinMaxScaler()
x_scaler = min_max_scaler.fit(x_train)
x_train = x_scaler.transform(x_train)
x_test = x_scaler.transform(x_test)

# minimum maximum *************************************************************************************************************************
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
    plt.show()

    # get feature importance
    feature_importance = model.feature_importances_

    # plot feature importance
    plt.bar([x_column_list[x] for x in range(len(feature_importance))], feature_importance)
    plt.xticks(rotation=90, ha='right')
    plt.title("Feature Importance")
    plt.xlabel("Features")
    plt.ylabel("Scores")
    plt.show()
# *****************************************************************************************************************************************

# buy or sell *****************************************************************************************************************************
elif y_type == 'buy or sell':
    # actions class count
    print('Actions Class Count:\n', dataset[y_column_list[0]].value_counts(), '\n\n')

    # balance classes using SMOTE *************************************************************************************
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
    # *****************************************************************************************************************

    # train model *****************************************************************************************************
    # create RF classifier model
    # model = RandomForestClassifier(n_estimators = 100, verbose=2, n_jobs=-1, random_state=seed)  
    # create XGBoost classifier model
    model = XGBClassifier(objective='multi:softprob', num_class=3, verbosity=2)

    # train model
    model.fit(x_train, y_train)
    
    # performing predictions on the test dataset
    y_predicted = model.predict(x_test)
    # *****************************************************************************************************************

    # decode the predictions back to the original string labels
    y_predicted = label_encoder.inverse_transform(y_predicted)

    # decode y_test back to the original string labels
    y_test = label_encoder.inverse_transform(y_test)

    # model perfomance ************************************************************************************************
    # using metrics module for accuracy calculation
    print('\n\nACCURACY OF THE MODEL:', accuracy_score(y_test, y_predicted), '\n\n')

    # print classification report for model
    print('CLASSIFICATION REPORT:\n', classification_report(y_test, y_predicted), '\n\n')

    # print confusion matrix
    confusion_matrix_ = pd.DataFrame(
        confusion_matrix(y_test, y_predicted, labels=['Buy', 'Nothing', 'Sell']), 
        index=['Buy (Actual)', 'Nothing (Actual)', 'Sell (Actual)'], 
        columns=['Buy (Predicted)', 'Nothing (Predicted)', 'Sell (Predicted)']
    )
    print('CONFUSION MATRIX:\n', confusion_matrix_, '\n\n')
    # *****************************************************************************************************************

    # visualize actual vs predicted ***********************************************************************************
    # replace all Buys with 1
    y_test[y_test == 'Buy'] = 1
    y_predicted[y_predicted == 'Buy'] = 1

    # replace all Nothings with 0
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
    plt.show()
    # *****************************************************************************************************************

    # feature importance **********************************************************************************************
    # get feature importance
    feature_importance = model.feature_importances_

    # plot feature importance
    plt.bar([x_column_list[x] for x in range(len(feature_importance))], feature_importance)
    plt.xticks(rotation=90, ha='right')
    plt.title("Feature Importance")
    plt.xlabel("Features")
    plt.ylabel("Scores")
    plt.show()
    # *****************************************************************************************************************
# *****************************************************************************************************************************************