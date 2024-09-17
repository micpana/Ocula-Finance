import getpass
import pickle
import traceback
from cryptography.fernet import Fernet
from settings import get_y_feature_engineering_object_path

"""
    fernet variable loaded with the key encryption key should come from calling module, ie x_y_feature_engineering or manage_expired_open_trades
"""

# decrypt the data
try:
    # decrypt y feature engineering file
    with open(get_y_feature_engineering_object_path(), 'rb') as file:
        loaded_data = pickle.loads(fernet.decrypt(file.read()))
    print('Key Accepted in Y Feature Engineering')

    # y feature engineering code execution
    try:
        exec(loaded_data['code'])
    except Exception as e:
        print('Y Feature Engineering Code Execution Error')

        # print the type of exception and a custom message
        print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

        # print the traceback details
        traceback.print_exc()

except:
    print('Key Rejected in Y Feature Engineering')