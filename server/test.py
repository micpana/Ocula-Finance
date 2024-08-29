import pandas as pd

dict = {
    'a': [1, 2, 3, 4, 5]
}

dataframe = pd.DataFrame(dict)
print(dataframe)
dataframe = dataframe.iloc[:-2]
print(dataframe)