from seeker import Seeker
import numpy as np

# x dataset
x = np.array([ 
    np.array([3, 4, 5, 6, 7]), 
    np.array([7, 6, 5, 4, 3]), 
    np.array([1, 4, 2, 6, 9]), 
    np.array([4, 3, 6, 5, 9]),
    np.array([7, 5, 6, 4, 3]),  
], dtype=float)

# y dataset
y = np.array([
    np.array(['8, 9']), 
    np.array(['2, 1']), 
    np.array(['4, 8']), 
    np.array(['8, 7']), 
    np.array(['2, 1']), 
], dtype=str)
print(y)

# x input ... to be used for predictions
input = np.array([3, 4, 5, 6, 7], dtype=float)

seeker = Seeker()
seeker.verbosity = True
seeker.regression = False
seek_result = seeker.seek(x, y, input)

print('Seek Result:', seek_result)

# x_test, y_test = x[3:, :], y[3:, :]

# seek_results = seeker.test(x, y, x_test, y_test)
# print('Seek Results:\n', seek_results)