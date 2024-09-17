import getpass
import pickle
import traceback
from cryptography.fernet import Fernet
from settings import get_x_y_feature_engineering_object_path

"""
    fernet variable loaded with the key encryption key should come from calling module, ie x_y_predict or x_y_train
"""

# add key to modules that also depend on it, ones that the encrypted code will call from this module **************************************
# module importations ***********************************************************************************************************
import x_feature_engineering
import y_feature_engineering
# *******************************************************************************************************************************
# setting the fernet variable in each of the modules ****************************************************************************
x_feature_engineering.fernet = fernet
y_feature_engineering.fernet = fernet
# *******************************************************************************************************************************
# *****************************************************************************************************************************************

# decrypt the data
try:
    # decrypt x y feature engineering file
    with open(get_x_y_feature_engineering_object_path(), 'rb') as file:
        loaded_data = pickle.loads(fernet.decrypt(file.read()))
    print('Key Accepted in X Y Feature Engineering')

    # x y feature engineering code execution
    try:
        exec(loaded_data['code'])
    except Exception as e:
        print('X Y Feature Engineering Code Execution Error')

        # print the type of exception and a custom message
        print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

        # print the traceback details
        traceback.print_exc()

except:
    print('Key Rejected in X Y Feature Engineering')