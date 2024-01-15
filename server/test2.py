import numpy as np

# Create a sample array
arr = np.arange(10)

# Calculate the split indices
split_idx = int((1-0.2) * len(arr))
print('Split indices:', split_idx)

# Split the array
arr1, arr2 = arr[:split_idx], arr[split_idx:]

print('Main array:', arr)
# Print the split arrays
print(f"Array 1: {arr1}")
print(f"Array 2: {arr2}")
