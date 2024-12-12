import numpy as np

# function for shifting array elements one step backwards 
def shift_array_elements_one_step_backwards(array):
    shifted_array = np.empty_like(arr, dtype=float)  # ensure dtype supports NaN
    shifted_array[-1] = np.nan  # last position gets NaN
    shifted_array[:-1] = arr[1:]  # shift elements

    # return shifted array
    return shifted_array

# Example array
arr = np.array([1, 2, 3, 4, 5])
new = shift_array_elements_one_step_backwards(arr)
print(shifted_array)
