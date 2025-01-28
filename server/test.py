import pandas as pd
from collections import deque

dictionary = {
    'cow': deque(['buy', 'buy', 'nothing', 'sell', 'nothing', 'buy']),
    'cat': deque(['observer', 'meow', 'eat', 'sit', 'hunt', 'run'])
}

df = pd.DataFrame(dictionary)

print(df)

df = df.loc[df['cow'] != 'nothing', :]

print(df)