import numpy as np

highs = np.array([1, 2, 2, 1, 0, 0, 2, 3, 4, 4, 3]) 

lows = np.array([1, 1, 1, 0, 0, 2, 3, 4, 3, 3, 4]) 

# find indices of structure highs (i.e., highest values in each consecutive sub-sequence)
structure_highs_indices = np.argwhere(np.diff(np.sign(highs - np.roll(highs, 1))) < 0).flatten()

# find indices of structure lows (i.e., lowest values in each consecutive sub-sequence)
structure_lows_indices = np.argwhere(np.diff(np.sign(lows - np.roll(lows, 1))) > 0).flatten()

# if high indices are consecutive, just take the last one
structure_highs_consecutive_indices = np.where(np.diff(structure_highs_indices) == 1)[0]
structure_highs_indices = structure_highs_indices[structure_highs_consecutive_indices + 1]

# if low indices are consecutive, just take the last one
structure_lows_consecutive_indices = np.where(np.diff(structure_lows_indices) == 1)[0]
structure_lows_indices = structure_lows_indices[structure_lows_consecutive_indices + 1]

# get the corresponding peak values using the structure highs indices
structure_highs = highs[structure_highs_indices]

# get the corresponding peak values using the structure lows indices
structure_lows = lows[structure_lows_indices]

print("Market structure highs:", structure_highs, '@', structure_highs_indices)
print("Market structure lows:", structure_lows, '@', structure_lows_indices)

