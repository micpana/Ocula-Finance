import getpass
import pickle
from cryptography.fernet import Fernet
from settings import get_feature_engineering_object_path

try: 
    # get feature engineering decryption key from user
    passkey = getpass.getpass("\n\nEnter Passkey (For Feature Engineering): ")
    feature_engineering_key = passkey.encode('utf-8')
    cipher_suite_feature_engineering = Fernet(feature_engineering_key)

    # decrypt the data
    try:
        # decrypt feature engineering file
        with open(get_feature_engineering_object_path(), 'rb') as file:
            loaded_data = pickle.loads(cipher_suite_feature_engineering.decrypt(file.read()))
        print('Feature Engineering Key Accepted')
 
        # feature engineering code execution
        try:
            exec(loaded_data['code'])
        except Exception as e:
            print('Code Execution Error')
            print(e)

    except:
        print('Feature Engineering Key Rejected')
        
except: 
    print('Invalid Key')