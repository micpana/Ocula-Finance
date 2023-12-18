import pandas as pd

# Replace this with your actual DataFrame
y_dataframe = pd.DataFrame({
    "col1": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
    "col2": [5, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 115],
})

y_description = y_dataframe.describe()
print('Description:\n', y_description)

string = """
it is:
{y_description}
""".format(y_description = y_description)

print(string)
