import numpy as np
from tqdm import tqdm
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
from collections import deque

class Seeker(object):
    def __init__(self):
        # parameters
        self.x = []
        self.y = []
        self.verbosity = True
        self.regression = True

    # function for seeking
    def seeker(self, input):
        # model parameters
        verbosity = self.verbosity
        regression = self.regression

        # compare corresponding columns per each row
        sequence_comparisons =  np.abs(input - self.x)

        # calculate weight value for each row based on column similarity figures
        sequence_row_sumations = sequence_comparisons.sum(axis=1) 

        # get the smallest value in sequence summations
        smallest_weight = np.nanmin(sequence_row_sumations) # ignore nans

        # find indexes of all rows holding the smallest weight we found
        indexes = np.where(sequence_row_sumations == smallest_weight)

        # get the real perceived values according to the indexes holding the smallest weight
        real_perceived_values = self.y[indexes]

        # get seek result
        unique, counts = np.unique(real_perceived_values, return_counts=True, axis=0) # arrays of unique values and their counts
        # print('y:', self.y)
        # print('sequence comparisons:', sequence_comparisons)
        # print('summations:', sequence_row_sumations)
        # print('smallest weight:', smallest_weight)
        # print('indexes:', indexes)
        # print('real:', real_perceived_values)
        # print('unique:', unique)
        # print('counts:', counts)
        counts_equal = np.all(counts == counts[0]) # check if the probabilities are equal
        if counts_equal == False: # if we have a single most probable outcome
            most_frequent_indices = np.argmax(counts, axis=0)
            seek_result = unique[most_frequent_indices]
        else: # if we have the same probabilities
            # for regression
            if regression == True:
                seek_result = np.mean(unique, axis=0)
            else: # for classification
                seek_result = unique[0]

        # return seek result, which = most frequent elements
        return seek_result

    # function for using seeker given a single input
    def seek(self, x, y, input):
        # set x and y as class parameters
        self.x = x
        self.y = y
        verbosity = self.verbosity

        # signal operation's start
        if verbosity == True:
            print('\n\nSeeking...\n\n')

        # seek
        seek_result = self.seeker(input)

        # return seek result
        return seek_result

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

        # initialize array to store seek_results
        seek_results = deque([])

        # loop through x_test
        for i in tqdm(range(0, len(x_test), +1), desc="Testing", unit="row", disable= not verbosity):
            # get current row's data
            test_input_row = x_test[i]

            # seek
            seek_result = self.seeker(test_input_row)

            # add seek result to seek results array
            seek_results.append(seek_result)

        # for regression
        if self.regression == True:
            seek_results = np.array(seek_results)
        else: # for classification
            seek_results = np.array(seek_results, dtype=str)

        # for regression
        if self.regression == True:
            # mean squared error
            mse = mean_squared_error(y_test, seek_results)

            # root mean squared error
            rmse = np.sqrt(mse)

            # mean absolute error
            mae = mean_absolute_error(y_test, seek_results)

            # performance results printing
            if verbosity == True:
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
        else: # for classification
            # results object
            results_object = {
                'seek_results': seek_results
            }

        # create empty space between seeker's printouts and any other console outputs that may come after
        if verbosity == True:
            print('\n\n')
        
        # return results object
        return results_object