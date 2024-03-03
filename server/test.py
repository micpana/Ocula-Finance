from seeker import Seeker
import numpy as np

# x dataset
x = np.array([ 
    np.array([3, 4, 5, 6, 7]), 
    np.array([4, 5, 6, 7, 8]), 
    np.array([1, 2, 3, 4, 5]), 
    np.array([5, 6, 7, 8, 9]), 
    np.array([7, 8, 9, 10, 11]), 
    np.array([2, 3, 4, 5, 6]),
    np.array([8, 9, 10, 11, 12]),
    np.array([6, 7, 8, 9, 10])
], dtype=float)

# y dataset
y = np.array([
    np.array([8, 8]), np.array([9, 9]), np.array([6, 6]), np.array([10, 10]), np.array([12, 12]), np.array([7, 7]), np.array([13, 13]), np.array([11, 11])
], dtype=float)

# x input ... to be used for predictions
input = np.array([3, 4, 5, 6, 7], dtype=float)

seeker = Seeker()
seeker.n_closest = 2
seeker.run_value_simulation = True
seeker.number_of_simulations = 10000
seeker. simulate_using_normalize_distribution = True
seeker.verbosity = True
seek_result = seeker.seek(x, y, input)

print('Seek Result:', seek_result)

x_test, y_test = x[3:, :], y[3:, :]

seek_results = seeker.test(x, y, x_test, y_test)
print('Seek Results:\n', seek_results)