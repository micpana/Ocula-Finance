import numpy as np

def get_last_five_items(arr):
    if len(arr) < 5:
        return arr
    else:
        return arr[-5:]

# Example usage:
array1 = np.array([1, 2, 3, 4, 5, 6, 7])
array2 = np.array([1, 2, 3])

# print(get_last_five_items(array1))  # Output: [3 4 5 6 7]
# print(get_last_five_items(array2))  # Output: [1 2 3]

i = 3  # i= 3, val = 4
av = 2
print(np.sum(array1[:i+1][-av:]))
