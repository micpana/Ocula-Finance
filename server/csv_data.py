from pandas import read_csv
from settings import get_training_price_data_csvs_folder_path, get_error_logs_path

# get data ********************************************************************************************************************************
def csv_fetch_data(symbol, timeframe):
    print('Fetching', symbol, timeframe, 'data from CSV ...')
    
    # folder and column names ***************************************************************************************************
    folder = get_training_price_data_csvs_folder_path()
    columns = ['time', 'open', 'high', 'low', 'close', 'col1', 'col2']
    # ***************************************************************************************************************************
    
    # import timeframe ohlc data ************************************************************************************************
    timeframe_ohlc_file_path = folder + symbol + timeframe + ".csv"
    timeframe_ohlc_df = read_csv(timeframe_ohlc_file_path, names=columns, encoding='utf-16')
    # ***************************************************************************************************************************

    print('CSV data fetched.\n\n')

    # set broker_company_name
    broker_company_name = 'Unavailable (Yahoo Finance)'

    # return timeframe ohlc df, broker_company_name
    return timeframe_ohlc_df, broker_company_name
# *****************************************************************************************************************************************