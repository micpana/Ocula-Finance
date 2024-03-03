import numpy as np
from tqdm import tqdm
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

class Seeker(object):
    def __init__(self):
        # parameters
        self.x = []
        self.y = []
        self.n_closest = 2
        self.run_value_simulation = True
        self.number_of_simulations = 100000
        self. simulate_using_normalize_distribution = True
        self.verbosity = True

    # function for seeking
    def seeker(self, input):
        # model parameters
        verbosity = self.verbosity
        n_closest = self.n_closest
        run_value_simulation = self.run_value_simulation
        number_of_simulations = self.number_of_simulations
        simulate_using_normalize_distribution = self.simulate_using_normalize_distribution
        current_column_index = self.current_column_index

        # NOTE ... we're getting x and y directly from class parameters using self.x and self.y inorder to reduce overhead of assigning data to new x and y local variables during loops eg when seeker is called by the test function

        # signal operation's start
        if verbosity == True:
            print('\n\nSeeking...')

        #  weigh similarities per each row and perform sumations for each row's column ... using abs((input value - row-column value) / input value)
        if verbosity == True:
            print('Weighing rows...')
        normalized_differences = np.abs((input - self.x) / np.max(self.x)) # calculate similarities in each column per each row
        normalized_differences = np.nan_to_num(normalized_differences, nan=0, posinf=0, neginf=0) # replace all nan and inf values with 0
        row_sumations = normalized_differences.sum(axis=1) # calculate weight value for each row based on column similarity figures

        # sort row sumations
        sorted_sumations = np.sort(row_sumations)

        # get n closest values in sorted_summations *****************************
        if verbosity == True:
            print('Finding best matches...')
        # get the n closest rows' weight values
        n_closest_values = sorted_sumations[:n_closest] 
        # create a boolean mask where each element of n_closest_values is compared to each element of row_sumations
        mask = n_closest_values[:, np.newaxis] == row_sumations
        # use np.where to find the indices where the mask is True
        indices = np.where(mask)
        # get the indexes of n closest values
        indexes_for_n_closest_values = indices[1]

        # obtain the real closest values using the obtained indexes ... from y's entire rows but column=current_column_index
        if verbosity == True:
            print('Obtaining real values...')
        real_closest_values = np.array([self.y[:, current_column_index][i] for i in indexes_for_n_closest_values if True], dtype=float)

        # run seek_result via basic estimation
        if run_value_simulation == False:
            # calculate mean
            seek_result = real_closest_values.mean()

        # run seek_result via Monte Carlo Simulation
        else:
            # get the smallest and larget values among the real closest values
            min_value = real_closest_values.min()
            max_value = real_closest_values.max()

            # if we're using a normalized distribution
            if simulate_using_normalize_distribution == True:
                # normalize real closest values
                normalized_values = np.array([(y - min_value) / (max_value - min_value) for y in real_closest_values], dtype=float)

                # get mean and standard deviation
                mean = normalized_values.mean()
                std = normalized_values.std()

                # run simulations
                if verbosity == True:
                    print('Simulating Outputs...')
                simulations = np.random.normal(mean, std, number_of_simulations)

                # change normalized simulations to our ordinary scale
                simulations = np.array([(y * (max_value - min_value)) + min_value for y in simulations], dtype=float)
                
                # use the mean of the simulated values as the seek_result
                seek_result = simulations.mean()
            
            # if we're not using a normalized distribution
            else:
                # run simulation
                if verbosity == True:
                    print('Simulating Outputs...')
                simulations = np.random.uniform(min_value, max_value, number_of_simulations) # we're adding abs(min_value) to max_value so as to include max_value during simulation ... abs(min_value) won't stray max simulated values away from the distribution of our values

                # use the mean of the simulated values as the seek_result
                seek_result = simulations.mean()

        # create empty space between seeker's printouts and any other console outputs that may come after
        if verbosity == True:
            print('\n\n')

        # return seek result
        return seek_result

    # function for using seeker given a single input
    def seek(self, x, y, input):
        # set x and y as class parameters
        self.x = x
        self.y = y

        # get number of columns y has
        y_column_count = len(y[0])

        # initialize array to store seek_results ... number of rows is one because this function is for single inputs
        seek_results = np.zeros((1, y_column_count))

        # loop through y columns
        for j in range(0, y_column_count, +1):
            # set current column index to class parameters
            self.current_column_index = j

            # seek
            seek_result = self.seeker(input)

            # add seeker result to seek_results array ... row index is 0 because this function is for single inputs
            seek_results[0, j] = seek_result

        # return seek results
        return seek_results

    # function for testing seeker
    def test(self, x, y, x_test, y_test):
        # test parameters
        verbosity = self.verbosity

        # disable class's main verbosity so that seeker function doesn't printout as it seekes each x row for each x_test row 
        self.verbosity = False # the verbosity of this current test function will remain intact since it has already been saved tp its own local verbosity variable 

        # set x and y as class parameters
        self.x = x
        self.y = y

        # signal operation's start
        if verbosity == True:
            print('\n\nTesting...')

        # get number of columns y has
        y_column_count = len(y[0])

        # initialize array to store seek_results
        seek_results = np.zeros((len(x_test), y_column_count))

        # loop through x_test
        for i in tqdm(range(0, len(x_test), +1), desc="Testing", unit="row", disable= not verbosity):
            # get current row's data
            test_input_row = x_test[i]

            # loop through y columns
            for j in range(0, y_column_count, +1):
                # set current column index to class parameters
                self.current_column_index = j

                # seek
                seek_result = self.seeker(test_input_row)

                # add seeker result to seek_results array
                seek_results[i, j] = seek_result

        # performance results printing
        if verbosity == True:
            # mean squared error
            mse = mean_squared_error(y_test, seek_results)

            # root mean squared error
            rmse = np.sqrt(mse)

            # mean absolute error
            mae = mean_absolute_error(y_test, seek_results)

            # print performance results
            print('\n\nMean Squared Error (MSE):', mse)
            print('Root Mean Squared Error (RMSE):', rmse)
            print('Mean Absolute Error (MAE):', mae, '\n\n')

        # results object
        results_object = {
            'seek_results': seek_results,
            'mse': mse,
            'rmse': rmse,
            'mae': mae
        }

        # create empty space between seeker's printouts and any other console outputs that may come after
        if verbosity == True:
            print('\n\n')
        
        # return results object
        return results_object