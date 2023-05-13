from pandas import read_csv

# get data
def fetch_data():

    # folder and column names
    folder = 'train_csvs/'
    columns = ['Date', 'Open', 'High', 'Low', 'Close', 'col1', 'col2']

    # import daily ohlc data
    daily_ohlc_file = folder + 'Daily' + ".csv"
    daily_ohlc_df = read_csv(daily_ohlc_file, names=columns, encoding='utf-16')
    del daily_ohlc_df['col1']
    del daily_ohlc_df['col2']

    # import h4 ohlc data
    h4_ohlc_file = folder + 'H4' + ".csv"
    h4_ohlc_df = read_csv(h4_ohlc_file, names=columns, encoding='utf-16')
    del h4_ohlc_df['col1']
    del h4_ohlc_df['col2']

    # import h1 ohlc data
    h1_ohlc_file = folder + 'H1' + ".csv"
    h1_ohlc_df = read_csv(h1_ohlc_file, names=columns, encoding='utf-16')
    del h1_ohlc_df['col1']
    del h1_ohlc_df['col2']

    # import m15 ohlc data
    m15_ohlc_file = folder + 'M15' + ".csv"
    m15_ohlc_df = read_csv(m15_ohlc_file, names=columns, encoding='utf-16')
    del m15_ohlc_df['col1']
    del m15_ohlc_df['col2']
