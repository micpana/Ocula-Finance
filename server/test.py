import yfinance as yf

# returned columns ... Date, Open, High, Low, Close, Volume, Dividends, Stock Splits

# Set the range and interval
start_date = '2022-01-01'
end_date = '2022-12-01'
interval = '1d' # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

# Get the OHLC data
eurusd = yf.Ticker('EURUSD=X')
ohlc_data = eurusd.history(start=start_date, end=end_date, interval=interval)

# Print the OHLC data
print(ohlc_data)