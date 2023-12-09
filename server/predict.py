import getpass
import pickle
import traceback
from cryptography.fernet import Fernet
from settings import get_prediction_object_path

try: 
    # get prediction decryption key from user
    passkey = getpass.getpass("\n\nEnter Passkey (For Prediction): ")
    prediction_key = passkey.encode('utf-8')
    cipher_suite_prediction = Fernet(prediction_key)

    # decrypt the data
    try:
        # decrypt prediction file
        with open(get_prediction_object_path(), 'rb') as file:
            loaded_data = pickle.loads(cipher_suite_prediction.decrypt(file.read()))
        print('Prediction Key Accepted')

        # prediction code execution
        try:
            exec(loaded_data['code'])
        except Exception as e:
            print('Prediction Code Execution Error')

            # print the type of exception and a custom message
            print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

            # print the traceback details
            traceback.print_exc()

    except:
        print('Prediction Key Rejected')
        
except: 
    print('Invalid Key')