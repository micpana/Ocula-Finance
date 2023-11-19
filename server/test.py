import importlib
import getpass
import pickle
from cryptography.fernet import Fernet
from settings import get_feature_engineering_object_path, get_training_object_path, get_classified_folder_name

# function to read python files and convert them to strings
def read_file(filename):
    with open(filename, 'r') as f:
        file_content = f.read()
    return file_content

# generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
print('\n\nKey: \n', key)

# code content
file_content = read_file(get_classified_folder_name() + '/app.py')

data = {
    'code': str(file_content)
}

# serialize the data, using pickle
pickle_object = pickle.dumps(data)

# encrypt the data
encrypted_data = cipher_suite.encrypt(pickle_object)

# save the encrypted data to a file
with open(get_feature_engineering_object_path(), 'wb') as file:
    file.write(encrypted_data)

# clear key and cipher suite
key = None
cipher_suite = None

try: 
    # get decryption key from user
    passkey = getpass.getpass("\n\nEnter Passkey: ")
    key = passkey.encode('utf-8')
    cipher_suite = Fernet(key)

    # decrypt the data
    try:
        with open(get_feature_engineering_object_path(), 'rb') as file:
            loaded_data = pickle.loads(cipher_suite.decrypt(file.read()))
        print('Key Accepted')

        # code execution
        try:
            print('\n\nCode Execution: ')
            exec(loaded_data['code'])
        except Exception as e:
            print('Code Execution Error')
            print(e)

    except:
        print('Key Rejected')
        
except: 
    print('Invalid Key')