import numpy as np

input = np.array([2, 5, 7])
row1 = np.array([0, 4, 6])
row2 = np.array([4, 6, 8])
row3 = np.array([3, 5, 7])
rows = np.array([row1, row2, row3])
val1 = abs((input-row1)/(input))
val1[val1 == np.inf] = 0
val1[np.isnan(val1)] = 0
val2 = abs((input-row2)/(input))
val2[val2 == np.inf] = 0
val2[np.isnan(val2)] = 0
val3 = abs((input-row3)/(input))
val3[val3 == np.inf] = 0
val3[np.isnan(val3)] = 0
print(val1, sum(val1))
print(val2, sum(val2))
print(val3, sum(val3))
# print(dir(np))
x = np.array([ 
    np.array([30, 4, 5, 6, 7]), # 0 ... -8
    np.array([40, 5, 6, 7, 8]), # 1 ... -7
    np.array([1, 2, 3, 4, 5]), # 2 ... -6
    np.array([5, 6, 7, 8, 9]), # 3 ... -5
    np.array([7, 8, 9, 10, 11]), # 4 ... -4
    np.array([20, 3, 4, 5, 6]), # 5 ... -3
    np.array([8, 9, 10, 11, 12]), # 6 ... -2
    np.array([6, 7, 8, 9, 10]) # 7 ... -1
], dtype=float)

# NOTE
print(x[:, 0][2])
print(x.min())
print(x.max())

print(np.random.randint(1, 10, 5))
print(np.random.uniform(-1.0, 0, 5))
print(np.random.normal(0.01, 0.1, 5))


input = np.array([30, 4, 5, 6, 7], dtype=float)

normalized_differences = np.abs((input - x) / np.max(x)) # value for abs((input value - row-column value) / max value in x)
normalized_differences = np.nan_to_num(normalized_differences, nan=0, posinf=0, neginf=0) # replace all nan and inf values with 0

print('normalized differences:\n', normalized_differences)

row_sumations = normalized_differences.sum(axis=1)

print('row summations:\n', row_sumations)

row_sumations = np.array([2, 3, 4, 3, 4, 2, 3])
n_closest_values = np.array([4, 2, 3])

# create a boolean mask where each element of n_closest_values is compared to each element of row_sumations
mask = n_closest_values[:, np.newaxis] == row_sumations

# use np.where to find the indices where the mask is True
indices = np.where(mask)

print('indices chatgpt:', indices)

# get the indexes of n closest values
indexes_for_n_closest_values = indices[1]

print('indexes chatgpt:', indexes_for_n_closest_values)

################################
