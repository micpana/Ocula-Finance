import numpy as np

def sma(values, period):
    sma = np.zeros_like(values, dtype=float)
    # Ensure that we only calculate SMA for periods where there is enough data
    for i in range(period - 1, len(values)):
        sma[i] = np.mean(values[i - period + 1:i + 1])
    return sma

# Example usage:
prices = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
period = 3
sma_values = sma(prices, period)
print(sma_values)
