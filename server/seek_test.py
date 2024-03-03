import matplotlib.pyplot as plt
from settings import get_symbols, get_timeframes_in_use, training_data_source, use_closing_prices_only, get_error_logs_path, show_plots_during_training
from data import get_data
from seeker import Seeker

def test(symbol):
    # timeframes in use
    timeframes = get_timeframes_in_use() # in descending order

    # get price data collection settings ... closing prices only / all ohlc prices
    closing_prices_only_status = use_closing_prices_only()

    # get dataframe / main dataset , x_column_list, y_column_1, and y_column_2
    dataframe, x_column_list, y_column_1, y_column_2 = get_data(
        symbol, # symbol for model being trained
        timeframes,  # timeframes in use
        training_data_source(), # where the data is supposed to come from ... seeker uses same data as the training module
        'training', # purpose, what the data is being used for ... training / predicting ... seeker uses same data as the training module
        closing_prices_only_status, # price data collection settings ... closing prices only / all ohlc prices
    )

    # create x and y dataframe
    x_dataframe = dataframe.filter(x_column_list)
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

    # initialize Seeker
    seeker = Seeker()

    # Seeker parameters
    seeker.n_closest = 3
    seeker.run_value_simulation = True
    seeker.number_of_simulations = 100000
    seeker. simulate_using_normalize_distribution = False
    seeker.verbosity = True

    # run test
    performance_results = seeker.test(x, y, x_test, y_test)
    print(symbol, ' Seek Results:\n', performance_results, '\n\n')

    # seek results
    seek_results = performance_results['seek_results']

    # performance results plotting
    if show_plots_during_training() == True:
        actual_max_down = y_test[:, 0]
        actual_max_up = y_test[:, 1]
        seek_max_down = seek_results[:, 0]
        seek_max_up = seek_results[:, 1]

        plt.plot(actual_max_down, label='Actual Max Down')
        plt.plot(actual_max_up, label='Actual Max Up')
        plt.plot(seek_max_down, label='Seek Max Down')
        plt.plot(seek_max_up, label='Seek Max Up')
        plt.title('Seek Results vs Actual Values')
        plt.legend()
        plt.show()

# get list of symbols
symbols = get_symbols()

# train models for each symbol
for symbol in symbols:
    print('\n\nRunning Seeker Test for', symbol, '............................................')
    test(symbol)