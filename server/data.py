import getpass
import pickle
import traceback
from cryptography.fernet import Fernet
from settings import get_data_object_path

try: 
    # get data decryption key from user
    passkey = getpass.getpass("\n\nEnter Passkey (For Data): ")
    data_key = passkey.encode('utf-8')
    cipher_suite_data = Fernet(data_key)

    # decrypt the data
    try:
        # decrypt data file
        with open(get_data_object_path(), 'rb') as file:
            loaded_data = pickle.loads(cipher_suite_data.decrypt(file.read()))
        print('Data Key Accepted')

        # data code execution
        try:
            exec(loaded_data['code'])
        except Exception as e:
            print('Data Code Execution Error')

            # print the type of exception and a custom message
            print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

            # print the traceback details
            traceback.print_exc()

    except:
        print('Data Key Rejected')
        
except: 
    print('Invalid Key')