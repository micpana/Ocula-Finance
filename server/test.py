import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Generate dummy data
num_points = 1000
entry_timeframe_dates = [datetime.now() - timedelta(minutes=5 * i) for i in range(num_points)]
entry_timeframe_dates = entry_timeframe_dates[::-1]  # Reverse to get chronological order

actual_buy_prices = np.random.uniform(low=100, high=150, size=num_points)
actual_sell_prices = np.random.uniform(low=100, high=150, size=num_points)
predicted_buy_prices = np.random.uniform(low=100, high=150, size=num_points)
predicted_sell_prices = np.random.uniform(low=100, high=150, size=num_points)
actual_takeprofits = np.random.uniform(low=150, high=200, size=num_points)
actual_stoplosses = np.random.uniform(low=80, high=100, size=num_points)
predicted_takeprofits = np.random.uniform(low=150, high=200, size=num_points)
predicted_stoplosses = np.random.uniform(low=80, high=100, size=num_points)

symbol = "AAPL"  # Dummy stock symbol

# Plotting setup
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.15)

# Plot actual buying and selling points as squares
ax.scatter(entry_timeframe_dates, actual_buy_prices, label='Actual Buys', color='blue', marker='s', s=5)
ax.scatter(entry_timeframe_dates, actual_sell_prices, label='Actual Sells', color='maroon', marker='s', s=5)

# Plot predicted buying and selling points as circles
ax.scatter(entry_timeframe_dates, predicted_buy_prices, label='Predicted Buys', color='blue', marker='o', s=5)
ax.scatter(entry_timeframe_dates, predicted_sell_prices, label='Predicted Sells', color='maroon', marker='o', s=5)

# Plot takeprofit and stoploss points for actual trades as squares
ax.scatter(entry_timeframe_dates, actual_takeprofits, label='Actual Takeprofits', color='green', marker='s', s=5)
ax.scatter(entry_timeframe_dates, actual_stoplosses, label='Actual Stoplosses', color='red', marker='s', s=5)

# Plot takeprofit and stoploss points for predicted trades as circles
ax.scatter(entry_timeframe_dates, predicted_takeprofits, label='Predicted Takeprofits', color='green', marker='o', s=5)
ax.scatter(entry_timeframe_dates, predicted_stoplosses, label='Predicted Stoplosses', color='red', marker='o', s=5)

# Formatting the x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y.%m.%d %H:%M'))
ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))

# Initial x-axis limits to show the first 325 points ... the number is coming from MT5's default zoom's candlestick count
ax.set_xlim(entry_timeframe_dates[0], entry_timeframe_dates[324])

# Add legend and labels
plt.xlabel('Date')
plt.ylabel('Price')
plt.title(symbol + ' Buy Sell OHLC Chart')
plt.legend(loc="upper right")
plt.xticks(rotation=90)
plt.tight_layout()

# Slider setup
ax_slider = plt.axes([0.2, 0.02, 0.6, 0.03], facecolor="lightgoldenrodyellow")
slider = Slider(
    ax=ax_slider,
    label='Scroll',
    valmin=0,
    valmax=len(entry_timeframe_dates) - 325,
    valinit=0,
    valstep=1
)

# Update function for slider
def update(val):
    start = int(slider.val)
    ax.set_xlim(entry_timeframe_dates[start], entry_timeframe_dates[start + 324])
    fig.canvas.draw_idle()

# Attach update function to slider
slider.on_changed(update)

# Show plot
plt.show()
