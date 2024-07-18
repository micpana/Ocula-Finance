import numpy as np

x = np.array([ 
    np.array([3, 4, 5, 6, 7]), 
    np.array([7, 6, 5, 4, 3]), 
    np.array([1, 4, 2, 6, 9]), 
    np.array([4, 3, 6, 5, 9]),
    np.array([7, 5, 6, 4, 3]),  
    np.array([4, 5, 6, 7, 8]),
    np.array([5, 6, 7, 8, 9]),
    np.array([10, 11, 12, 13, 14]),
    np.array([14, 13, 12, 11, 10])
], dtype=float)

input = np.array([3, 4, 5, 3, 7], dtype=float)

# get number of samples and number of columns / features in x
n_samples, n_features = x.shape 

x_grid, input_grid = np.meshgrid(x, input, indexing='ij') # create grids using meshgrid
comparisons = (x_grid - input_grid) / np.max(x) # perform element-wise comparison
reshaped_comparisons = comparisons.reshape(n_samples, n_features, n_features) # reshape comparisons, separate rows to get back to x length... result will be of shape: (number of samples, comparisons per row, columns / features)
row_pair_weights = reshaped_comparisons.sum(axis=2) # sum up each row's column comparisons
row_weights = row_pair_weights.sum(axis=1) # sum up each rows's column comparison weights into one value
row_weights = np.abs(row_weights) # making the values absolute

print(row_weights)
print(input.shape)
print(np.min(input))