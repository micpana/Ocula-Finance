from data_acquisition import acquire_data
from x_feature_engineering import engineer_x
from y_feature_engineering import engineer_y
import pandas as pd

def engineer_x_y(symbol, y_type):
    # state timeframes
    timeframes = [
        'Daily', 
        'H4', 
        'H1', 
        'M30',
        'M15'
    ]

    # number of most recent turning points per each view window
    number_of_most_recent_turning_points_per_each_view_window = 3

    # get dataframes
    daily_df, h4_df, h1_df, m30_df, m15_df = acquire_data(symbol, timeframes)

    # get x_features_dataframe
    x_features_dataframe, x_column_list = engineer_x(daily_df, h4_df, h1_df, m30_df, m15_df)

    # get y_features_dataframe
    y_features_dataframe, y_column_list = engineer_y(x_features_dataframe, y_type)

    # combine x and y feature dataframes
    x_y_feature_dataframe = pd.concat([x_features_dataframe, y_features_dataframe], axis=1)

    # return x_y_feature_dataframe
    return x_y_feature_dataframe, x_column_list, y_column_list