list_of_symbols = ['EURUSD', 'GBPJPY', 'USDCHF']
# symbol selection prompt
symbol_selection_prompt = 'Select a symbol by its listed number from the options below:\n'
for i in range(len(list_of_symbols)):
    symbol = list_of_symbols[i]
    symbol_selection_prompt = symbol_selection_prompt + str(i+1) + '. ' + symbol + '\n'
# add text at the bottom of the symbol selection prompt
symbol_selection_prompt = symbol_selection_prompt + '\nYour selection: '
# ask user to select a symbol to run a backtest on
user_number_selection = input(symbol_selection_prompt)
# user selected symbol
user_selected_symbol = list_of_symbols[int(user_number_selection)-1]
print('\n\nRunning a backtest on:', user_selected_symbol)