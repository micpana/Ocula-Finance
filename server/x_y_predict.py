import getpass
import pickle
import traceback
from cryptography.fernet import Fernet
from settings import get_x_y_prediction_object_path

try: 
    # get key from user
    passkey = getpass.getpass("\n\nEnter Passkey: ")
    key = passkey.encode('utf-8')
    fernet = Fernet(key)

    # add key to modules that also depend on it, ones that the encrypted code will call from this module **********************************
    # module importations *******************************************************************************************************
    import x_y_feature_engineering
    import manage_expired_open_trades
    # ***************************************************************************************************************************
    # setting the fernet variable in each of the modules ************************************************************************
    x_y_feature_engineering.fernet = fernet
    manage_expired_open_trades.fernet = fernet
    # ***************************************************************************************************************************
    # *************************************************************************************************************************************

    # decrypt the data
    try:
        # decrypt x y prediction file
        with open(get_x_y_prediction_object_path(), 'rb') as file:
            loaded_data = pickle.loads(fernet.decrypt(file.read()))
        print('Key Accepted in X Y Predict')

        # x y prediction code execution
        try:
            exec(loaded_data['code'])
        except Exception as e:
            print('X Y Predict Code Execution Error')

            # print the type of exception and a custom message
            print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

            # print the traceback details
            traceback.print_exc()

    except:
        print('Key Rejected in X Y Predict')
        
except: 
    print('Invalid Key')