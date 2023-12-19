import numpy as np

timeframe_3_dates = np.array([1, 2, 3, 4, 5, 6, 7])
timeframe_4_date = 6
timeframe_3_index_of_date_reference = np.where(timeframe_3_dates <= timeframe_4_date)[0][-1]

print('index:', timeframe_3_index_of_date_reference)
print(np.where(timeframe_3_dates <= timeframe_4_date)[0])