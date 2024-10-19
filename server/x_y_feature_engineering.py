import getpass
import pickle
import traceback
from cryptography.fernet import Fernet
from settings import get_x_y_feature_engineering_object_path

# decrypt the data
try:
    # get key from user
    passkey = getpass.getpass("\n\nEnter Passkey (X Y Feature Engineering): ")
    key = passkey.encode('utf-8')
    fernet = Fernet(key)

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
    print('Key Rejected in X Y Feature Engineering / File Not Found')