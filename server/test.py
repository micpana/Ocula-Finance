from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

ls_1 = [1, 2, 3, 4, 5 ,6, 7]
ls_2 = [3, 4, 5, 6, 7, 8, 9]

mae = mean_absolute_error(ls_1, ls_2)
rmse = np.sqrt(mean_squared_error(ls_1, ls_2))
mse = mean_squared_error(ls_1, ls_2)
print(mae)
print(rmse)
print(mse)