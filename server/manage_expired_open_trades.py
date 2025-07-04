import getpass
import pickle
import traceback
from cryptography.fernet import Fernet
from settings import get_manage_expired_open_trades_object_path

# decrypt the data
try:
    # get key from user
    passkey = getpass.getpass("\n\nEnter Passkey (Manage Expired Open Trades): ")
    key = passkey.encode('utf-8')
    fernet = Fernet(key)

    # decrypt manage expired open trades file
    with open(get_manage_expired_open_trades_object_path(), 'rb') as file:
        loaded_data = pickle.loads(fernet.decrypt(file.read()))
    print('Key Accepted in Manage Expired Open Trades')

    # manage expired open trades code execution
    try:
        exec(loaded_data['code'])
    except Exception as e:
        print('Manage Expired Open Trades Code Execution Error')

        # print the type of exception and a custom message
        print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

        # print the traceback details
        traceback.print_exc()

except:
    print('Key Rejected in Manage Expired Open Trades / File Not Found')