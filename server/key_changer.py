import os
import getpass
from cryptography.fernet import Fernet
from settings import get_x_y_feature_engineering_object_path, get_x_feature_engineering_object_path, get_y_feature_engineering_object_path, get_x_y_prediction_object_path, get_x_y_training_object_path, get_manage_expired_open_trades_object_path, get_scaler_path, get_model_path
from symbol_config import get_symbol_list

# optional list of other encrypted files to reencrypt apart from scalers and models (these are reencrypted by default) ********************
other_encrypted_files_to_reencrypt = [
    # get_x_y_feature_engineering_object_path(), 
    # get_x_feature_engineering_object_path(), 
    # get_y_feature_engineering_object_path(), 
    # get_x_y_prediction_object_path(), 
    # get_x_y_training_object_path(), 
    # get_manage_expired_open_trades_object_path(),
]
# *****************************************************************************************************************************************

# get list of symbols *********************************************************************************************************************
list_of_symbols = get_symbol_list()
# printout the list of symbols being used
print('\n\nRunning reencryption for the following symbols:', list_of_symbols)
# *****************************************************************************************************************************************

try:
    # get old key from user
    passkey = getpass.getpass("\n\nEnter Passkey (Old): ")
    key = passkey.encode('utf-8')
    old_fernet = Fernet(key)

    # get old key from user
    passkey = getpass.getpass("\n\nEnter Passkey (New): ")
    key = passkey.encode('utf-8')
    new_fernet = Fernet(key)

    # reencryption function *****************************************************************************************************
    def reencrypt(encrypted_file_name):
        # printout current encryption stage
        print('\n\nRe-encrypting', encrypted_file_name)
        try:
            # decrypt encrypted file using old key
            with open(encrypted_file_name, 'rb') as file:
                decrypted_file = old_fernet.decrypt(file.read())
            print('Old Key Accepted.')
            # encrypt decrypted data using new key
            encrypted_data = new_fernet.encrypt(decrypted_file)
            print('New Key Accepted.')
            # save the encrypted data back to the file
            with open(os.path.join('..', encrypted_file_name), 'wb') as file:
                file.write(encrypted_data)
            # notify user of reencryption completion
            print('Done!')
            print('Saved to:', encrypted_file_name)
        except:
            print('Key Rejected / File Not Found')
    # ***************************************************************************************************************************

        
    # reencrypt scalers and models for all symbols ******************************************************************************
    print('\n\nRe-encrypting symbol files (scalers and models)...')
    for symbol in list_of_symbols:
        # scaler path
        scaler_path = get_scaler_path(symbol)
        # model path
        model_path = get_model_path(symbol)
        # reencrypt scaler
        reencrypt(scaler_path)
        # reencrypt model
        reencrypt(model_path)
    print('\n\nDone with symbol files.')
    # ***************************************************************************************************************************

    # loop through other encrypted files re-encrypting them *********************************************************************
    index = 1
    for encrypted_file_name in other_encrypted_files_to_reencrypt:
        # printout current encryption stage
        print('\n\nRe-encrypting', encrypted_file_name, '(', index, '/', len(other_encrypted_files_to_reencrypt), ')', '...')
        # increment index
        index = index + 1
        # reencrypt file
        reencrypt(encrypted_file_name)
    # ***************************************************************************************************************************
        
except: 
    print('Invalid Key')