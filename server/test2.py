import numpy as np
timeframe_2_dates = np.array([1, 2, 3], dtype=int)
timeframes = np.array([1, 2, 3], dtype=int)
most_recent_first_date_found = 0
if len(timeframes) >= 2: 
    if timeframe_2_dates[2:][0] > most_recent_first_date_found: most_recent_first_date_found = timeframe_2_dates[2:][0]
print(most_recent_first_date_found)