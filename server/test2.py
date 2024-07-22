import numpy as np

def calculate_atr(high, low, close, period=14):
    print(period)
    quit()
    # Calculate the True Range (TR)
    high_low = high - low
    high_close = np.abs(high - np.roll(close, 1))
    low_close = np.abs(low - np.roll(close, 1))

    tr = np.maximum(high_low, high_close)
    tr = np.maximum(tr, low_close)
    tr[0] = 0  # Set the first element to 0 since there's no previous close for the first period

    # Calculate the ATR
    atr = np.zeros_like(close)
    atr[period-1] = np.mean(tr[:period])  # First ATR value is the mean of the first 'period' TR values

    for i in range(period, len(close)):
        atr[i] = (atr[i-1] * (period - 1) + tr[i]) / period

    return atr

# Example usage
high = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25])
low = np.array([9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24])
close = np.array([9.5, 10.5, 11.5, 12.5, 13.5, 14.5, 15.5, 16.5, 17.5, 18.5, 19.5, 20.5, 21.5, 22.5, 23.5, 24.5])

atr = calculate_atr(high, low, close, period=50)
print("14-period ATR:", atr)
