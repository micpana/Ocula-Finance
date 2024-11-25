import numpy as np

trade_entry_timeframe_timestamp = '2024.11.23 12:00'
trade_action = 'Buy'

timestamps = np.array(['2024.11.23 10:00', '2024.11.23 12:00', '2024.11.23 14:00'])
actual_trading_actions = np.array(['Sell', 'Buy', 'Sell'])

trade_index_array = np.where(
    (timestamps == trade_entry_timeframe_timestamp) & 
    (actual_trading_actions == trade_action)
)[0]

print(trade_index_array[0])
