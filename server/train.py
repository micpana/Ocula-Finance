import getpass
import pickle
from cryptography.fernet import Fernet
from settings import get_training_object_path, get_prediction_object_path

try: 
    # get training decryption key from user
    passkey = getpass.getpass("\n\nEnter Passkey (For Training): ")
    training_key = passkey.encode('utf-8')
    cipher_suite_training = Fernet(training_key)

    # get prediction decryption key from user
    passkey = getpass.getpass("\n\nEnter Passkey (For Prediction): ")
    prediction_key = passkey.encode('utf-8')
    cipher_suite_prediction = Fernet(prediction_key)

    # decrypt the data
    try:
        # decrypt training file
        with open(get_training_object_path(), 'rb') as file:
            loaded_data = pickle.loads(cipher_suite_training.decrypt(file.read()))
        print('Training Key Accepted')

        # validate prediction_key
        try:
            # decrypt prediction file
            with open(get_prediction_object_path(), 'rb') as file:
                cipher_suite_prediction.decrypt(file.read())
            print('Prediction Key Accepted')

            # training code execution
            try:
                exec(loaded_data['code'])
            except Exception as e:
                print('Code Execution Error')
                print(e)

        except:
            print('Prediction Key Rejected')

    except:
        print('Training Key Rejected')
        
except: 
    print('Invalid Key')