import pandas as pd

# Sample DataFrame
data = {'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]}
df = pd.DataFrame(data)

# Column list with an extra column 'D'
column_list = ['A', 'B', 'D', 'J']

# Filter the DataFrame
filtered_df = df.filter(column_list)

print(filtered_df)