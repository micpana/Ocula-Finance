from tqdm import tqdm
import arch  # or arch.univariate
# from copulas.multivariate import GaussianMultivariate
from scipy.stats import norm
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from csv_data import csv_fetch_data
from yahoo_finance_data import yahoo_fetch_data
from settings import get_data_collection_days_by_intended_purpose, get_forecast_period, remove_last_n_values_without_full_forecast, incorporate_simulation, number_of_candlesticks_to_simulate, number_of_simulations, aggregate_across_simulations, show_plots_during_training, show_simulated_price_chart
from feature_engineering import get_feature_dataset

# get data
def get_data(symbol, timeframes, source, purpose, closing_prices_only_status):

    # get data collection days by intended purpose
    data_collection_days = get_data_collection_days_by_intended_purpose(purpose)

    # collect data by purpose
    if source == 'csv':
        timeframe_1_ohlc_df, timeframe_2_ohlc_df, timeframe_3_ohlc_df, timeframe_4_ohlc_df, timeframe_5_ohlc_df, timeframe_6_ohlc_df, timeframe_7_ohlc_df, timeframe_8_ohlc_df = csv_fetch_data(symbol, timeframes, data_collection_days)

    elif source == 'mt5':
        # mt5 python module is only available on Windows so import was placed here to avoid encountering import errors on other OSes
        from mt5_data import mt5_fetch_data
        timeframe_1_ohlc_df, timeframe_2_ohlc_df, timeframe_3_ohlc_df, timeframe_4_ohlc_df, timeframe_5_ohlc_df, timeframe_6_ohlc_df, timeframe_7_ohlc_df, timeframe_8_ohlc_df =  mt5_fetch_data(symbol, timeframes, data_collection_days)

    elif source == 'yahoo':
        timeframe_1_ohlc_df, timeframe_2_ohlc_df, timeframe_3_ohlc_df, timeframe_4_ohlc_df, timeframe_5_ohlc_df, timeframe_6_ohlc_df, timeframe_7_ohlc_df, timeframe_8_ohlc_df =  yahoo_fetch_data(symbol, timeframes, data_collection_days)

    # use Monte Carlo (with Geometric Brownina Motion and GARCH)to simulate n price paths, for the smallest timeframe only, and during training operations only ... if enabled
    if purpose == 'training' and incorporate_simulation() == True:
        print('\n\nPreparing to simulate...')
        # dataframe to simulate (smallest timeframe's dataset)
        if len(timeframes) >= 1: smallest_timeframe_df = timeframe_1_ohlc_df
        if len(timeframes) >= 2: smallest_timeframe_df = timeframe_2_ohlc_df
        if len(timeframes) >= 3: smallest_timeframe_df = timeframe_3_ohlc_df
        if len(timeframes) >= 4: smallest_timeframe_df = timeframe_4_ohlc_df
        if len(timeframes) >= 5: smallest_timeframe_df = timeframe_5_ohlc_df
        if len(timeframes) >= 6: smallest_timeframe_df = timeframe_6_ohlc_df
        if len(timeframes) >= 7: smallest_timeframe_df = timeframe_7_ohlc_df
        if len(timeframes) >= 8: smallest_timeframe_df = timeframe_8_ohlc_df
        smallest_timeframe_df = smallest_timeframe_df.tail(50) ###########################################*****************************

        # load historical returns data (log returns)
        print('Loading historical returns...')
        closes = smallest_timeframe_df['close'].values
        returns = np.log(closes[1:] / closes[:-1])

        # parameters for GBM
        print('Creating simulation parameters...')
        S0 = closes[-1]  # initial price
        mu = returns.mean()  # drift rate (expected return / mean)
        T = number_of_candlesticks_to_simulate()  # number of candlesticks to simulate per simulation
        dt = 1 / T  # Time step
        num_simulations = number_of_simulations() # number of simulations to run
        
        # fit GARCH model
        print('Modeling volatility...')
        garch_model = arch.arch_model(returns, p=1, q=1)
        garch_model_fit = garch_model.fit(disp="off")
        
        # simulate prices with time-varying volatility
        np.random.seed(42)  # set seed for reproducibility
        W = np.random.randn(num_simulations, T + 1)
        S = np.zeros((num_simulations, T + 1))
        S[:, 0] = S0
        sigma = garch_model_fit.conditional_volatility[0]  # initialize volatility
        for t in tqdm(range(1, T + 1), desc="Price Simulation", unit="path"):
            sigma = garch_model_fit.forecast(horizon=1).variance.values[0]  # update volatility
            S[:, t] = S[:, t - 1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * W[:, t])

        # create dataFrame for simulated closing prices
        simulated_closing_prices = pd.DataFrame(S)
        
        # extract relevant data for Copula fitting from smallest timeframe df ... closes have already been extracted above
        opens = smallest_timeframe_df['open'].values
        highs = smallest_timeframe_df['high'].values
        lows = smallest_timeframe_df['low'].values
        
        # choose and fit a suitable Copula (e.g., Gaussian)
        print('Modeling price relations...')
        copula = GaussianMultivariate()
        copula.fit(np.array([opens, highs, lows, closes]))
        
        # simulate uniform marginals from copula
        u = copula.sample(num_simulations)
        
        # convert uniform marginals to standard normal marginals
        z = norm.ppf(u)

        print('\n\nU:', len(u), '\n\n', u)
        print('Z:', len(z), '\n\n', z)
        print('S:', len(simulated_closing_prices.iloc[1:, :]), '\n\n', simulated_closing_prices.iloc[1:, :], '\n\n')
        
        # simulate opening, high, and low prices
        print('Simulating price relations...')
        simulated_opening_prices = simulated_closing_prices.shift(1).iloc[1:, :] * np.exp(-0.5 * sigma**2 * dt + sigma * np.sqrt(dt) * z[:, 0])
        simulated_high_prices = simulated_closing_prices.shift(1).iloc[1:, :] * np.exp(-0.5 * sigma**2 * dt + sigma * np.sqrt(dt) * z[:, 1])
        simulated_low_prices = simulated_closing_prices.shift(1).iloc[1:, :] * np.exp(-0.5 * sigma**2 * dt + sigma * np.sqrt(dt) * z[:, 2])
        
        # simulation start date
        simulation_start_date = '1970-01-01'

        # function to get timeframe frequency for pandas
        def timeframe_frequency(timeframe):
            if timeframe == 'Monthly': frequency = 'M'
            elif timeframe == 'Weekly': frequency = 'W'
            elif timeframe == 'Daily': frequency = 'D'
            elif timeframe == 'H4': frequency = '4H'
            elif timeframe == 'H1': frequency = 'H'
            elif timeframe == 'M30': frequency = '30T'
            elif timeframe == 'M15': frequency = '15T'
            elif timeframe == 'M5': frequency = '5T'
            elif timeframe == 'M1': frequency = 'T'

            return frequency
        
        # determine date_range frequency given the smallest timeframe's name 
        smallest_timeframe = timeframes[-1]
        frequency = timeframe_frequency(smallest_timeframe)

        # whether to aggregate across simulations or not ... if aggregating, the resulting dataFrame provides a condensed overview of the simulated price movements, summarizing the central tendencies of all simulations for each time step ... if not aggregating, resulting dataframe will have num_simulations * T rows
        if aggregate_across_simulations() == True:
            print('Aggregating...')
            # create dataFrame for opening, high, and low prices
            ohlc_prices = pd.DataFrame({
                            'time': pd.date_range(start=simulation_start_date, periods=T, freq=frequency),
                            'open': simulated_opening_prices.mean(axis=1),
                            'high': simulated_high_prices.max(axis=1),
                            'low': simulated_low_prices.min(axis=1),
                            'close': simulated_closing_prices.iloc[1:, :].mean(axis=1)
                        })
        else: # not aggregating across simulations but rather including all simulations as they are (num_simulations * T)
            print('Joining...')
            # get continuous simulated prices *************************************
            # array initializations
            continuous_simulated_opening_prices = np.zeros((num_simulations * T))
            continuous_simulated_high_prices = np.zeros((num_simulations * T))
            continuous_simulated_low_prices = np.zeros((num_simulations * T))
            continuous_simulated_closing_prices = np.zeros((num_simulations * T))
            # loop through simulation rows
            for i in tqdm(range(0, num_simulations * T, +T), desc="Joining simulations", unit="row"):
                # loop through current row's columns
                for j in range(T):
                    # get price index
                    if i < T: prices_index = 0
                    else: prices_index = int(i/T)
                    # value extraction
                    continuous_simulated_opening_prices[i+j] = simulated_opening_prices.values[prices_index][j]
                    continuous_simulated_high_prices[i+j] = simulated_high_prices.values[prices_index][j]
                    continuous_simulated_low_prices[i+j] = simulated_low_prices.values[prices_index][j]
                    continuous_simulated_closing_prices[i+j] = simulated_closing_prices.iloc[1:, :].values[prices_index][j]

            # create dataFrame for opening, high, and low prices
            ohlc_prices = pd.DataFrame({
                            'time': pd.date_range(start=simulation_start_date, periods=num_simulations*T, freq=frequency),
                            'open': continuous_simulated_opening_prices,
                            'high': continuous_simulated_high_prices,
                            'low': continuous_simulated_low_prices,
                            'close': continuous_simulated_closing_prices
                        })
                    
        # print resulting simulated ohlc dataframe
        print('\n\nSimulated OHLC:\n', ohlc_prices, '\n\n')
            
        # set the datetime index if its not already set ... for resampling purposes
        ohlc_prices['time'] = pd.to_datetime(ohlc_prices['time'])
        ohlc_prices.set_index('time', inplace=True)

        # plot simulated ohlc data
        if show_plots_during_training() == True and show_simulated_price_chart() == True:
            # plotting candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x = ohlc_prices['time'],
                open = ohlc_prices['open'],
                high = ohlc_prices['high'],
                low = ohlc_prices['low'],
                close = ohlc_prices['close']
            )])
            
            # set chart layout
            fig.update_layout(
                title = 'Simulated Candlestick Chart',
                xaxis_title = 'Time',
                yaxis_title = 'Price',
                xaxis_rangeslider_visible = False
            )
            
            # Show the chart
            fig.show()

        # function for resampling df to needed timeframe df
        def resample_df(timeframe_index):
            # timeframe name
            timeframe_name = timeframes[timeframe_index]

            # if current timeframe's name is the smallest timeframe, return simulated df as is, no need to resample
            if timeframe_name == smallest_timeframe:
                return ohlc_prices

            else:
                # get pandas resample rule / frequency
                frequency = timeframe_frequency(timeframe_name)

                # get resampled df
                resampled_df = ohlc_prices.resample(frequency).agg({'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'})

                # drop any rows with missing data
                resampled_df.dropna(inplace=True)

                # reset the indexes if needed
                resampled_df.reset_index(inplace=True)

                return resampled_df

        # assign simulated data to each present timeframe
        print('Resampling...')
        if len(timeframes) >= 1: simulated_timeframe_1_ohlc_df = resample_df(0)
        if len(timeframes) >= 2: simulated_timeframe_2_ohlc_df = resample_df(1)
        if len(timeframes) >= 3: simulated_timeframe_3_ohlc_df = resample_df(2)
        if len(timeframes) >= 4: simulated_timeframe_4_ohlc_df = resample_df(3)
        if len(timeframes) >= 5: simulated_timeframe_5_ohlc_df = resample_df(4)
        if len(timeframes) >= 6: simulated_timeframe_6_ohlc_df = resample_df(5)
        if len(timeframes) >= 7: simulated_timeframe_7_ohlc_df = resample_df(6)
        if len(timeframes) >= 8: simulated_timeframe_8_ohlc_df = resample_df(7)

        # combine real data and simulated data ... simulated data should be placed before real data ... test set + date matching code depends on it ... our test set should contain real data, the more the better
        print('Combining dataframes...\n\n')
        if len(timeframes) >= 1: timeframe_1_ohlc_df = pd.concat([simulated_timeframe_1_ohlc_df, timeframe_1_ohlc_df], ignore_index=True) # reset index if needed
        if len(timeframes) >= 2: timeframe_2_ohlc_df = pd.concat([simulated_timeframe_2_ohlc_df, timeframe_2_ohlc_df], ignore_index=True) # reset index if needed
        if len(timeframes) >= 3: timeframe_3_ohlc_df = pd.concat([simulated_timeframe_3_ohlc_df, timeframe_3_ohlc_df], ignore_index=True) # reset index if needed
        if len(timeframes) >= 4: timeframe_4_ohlc_df = pd.concat([simulated_timeframe_4_ohlc_df, timeframe_4_ohlc_df], ignore_index=True) # reset index if needed
        if len(timeframes) >= 5: timeframe_5_ohlc_df = pd.concat([simulated_timeframe_5_ohlc_df, timeframe_5_ohlc_df], ignore_index=True) # reset index if needed
        if len(timeframes) >= 6: timeframe_6_ohlc_df = pd.concat([simulated_timeframe_6_ohlc_df, timeframe_6_ohlc_df], ignore_index=True) # reset index if needed
        if len(timeframes) >= 7: timeframe_7_ohlc_df = pd.concat([simulated_timeframe_7_ohlc_df, timeframe_7_ohlc_df], ignore_index=True) # reset index if needed
        if len(timeframes) >= 8: timeframe_8_ohlc_df = pd.concat([simulated_timeframe_8_ohlc_df, timeframe_8_ohlc_df], ignore_index=True) # reset index if needed
    
    # perform feature engineering
    engineered_dataset, x_column_list, y_column_1, y_column_2, entry_timeframe_last_datetime = get_feature_dataset(
        timeframes, # list of timeframes in use ... 4 timeframes ... listed in descending order
        timeframe_1_ohlc_df, # timeframe 1 ohlc dataframe
        timeframe_2_ohlc_df, # timeframe 2 ohlc dataframe
        timeframe_3_ohlc_df, # timeframe 3 ohlc dataframe
        timeframe_4_ohlc_df, # timeframe 4 ohlc dataframe
        timeframe_5_ohlc_df, # timeframe 5 ohlc dataframe
        timeframe_6_ohlc_df, # timeframe 6 ohlc dataframe
        timeframe_7_ohlc_df, # timeframe 7 ohlc dataframe
        timeframe_8_ohlc_df, # timeframe 8 ohlc dataframe
        closing_prices_only_status, # price data collection settings ... closing prices only / all ohlc prices
    )

    # return engineered dataset as per purpose
    if purpose == 'training':
        # get forecast period
        forecast = get_forecast_period()
        
        # removal of last n (n = forecast value) values without a full forecast view
        if remove_last_n_values_without_full_forecast() == True:
            engineered_dataset = engineered_dataset.iloc[:-forecast]

        # dataframe sample ... only print when absolutely necessary
        # print('\n\nX Dataframe:', engineered_dataset.filter(x_column_list).tail(8))

        # y dataframe sample
        print('\n\nY Dataframe:', engineered_dataset.filter([y_column_1, y_column_2]).tail(8))
        
        # return expected data
        return engineered_dataset, x_column_list, y_column_1, y_column_2
    else:
        # return expected data
        return engineered_dataset, entry_timeframe_last_datetime