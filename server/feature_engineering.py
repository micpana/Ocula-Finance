import getpass
import pickle
from cryptography.fernet import Fernet
from settings import get_feature_engineering_object_path

# get decryption key from user
passkey = getpass.getpass("\n\nEnter Passkey (For Feature Engineering): ")
key = passkey.encode('utf-8')
cipher_suite = Fernet(key)

try: 
    # decrypt the data
    try:
        with open(get_feature_engineering_object_path(), 'rb') as file:
            loaded_data = pickle.loads(cipher_suite.decrypt(file.read()))
        print('Key Accepted')
 
        # code execution
        try:
            exec(loaded_data['code'])
        except Exception as e:
            print('Code Execution Error')
            print(e)

    except:
        print('Key Rejected')
        
except: 
    print('Invalid Key')