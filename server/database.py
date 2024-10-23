from models import Users
import mongoengine
from mongoengine import connect, connection, get_connection, disconnect
from mongomock import MongoClient
import dns
import urllib
from encryption import encrypt_password, verify_encrypted_password
from datetime import datetime
import os
from settings import database_selection

# get live database credentials from environment variables
live_db_username = os.environ.get('LIVE_DB_USERNAME')
live_db_password = os.environ.get('LIVE_DB_PASSWORD')
live_db_url = os.environ.get('LIVE_DB_URL')

# get test database credentials from environment variables
test_db_username = os.environ.get('TEST_DB_USERNAME')
test_db_password = os.environ.get('TEST_DB_PASSWORD')

# get selected database ... mock / test / live
selected_database = database_selection()

# function to connect to the database *****************************************************************************************************
def connect_to_database():
    if selected_database == 'mock':
        # mock db connection
        client = MongoClient(mongo_client_class=MongoClient, db_name="ocula-finance-mock")
        port = client.address[1]
        connect(host=f"localhost:{port}", mongo_client_class=MongoClient)
    elif selected_database == 'test':
        # test db connection
        connect_url = 'mongodb://'+test_db_username+':'+urllib.parse.quote(test_db_password)+'@localhost:27017/ocula-finance-test'
        connect(host=connect_url)
    elif selected_database == 'live':
        # live db connection
        connect_url = 'mongodb+srv://'+live_db_username+':'+urllib.parse.quote(live_db_password)+live_db_url
        connect(host=connect_url, ssl=True, ssl_cert_reqs='CERT_NONE') # removed ssl=True, ssl_cert_reqs='CERT_NONE', in favor of tls=True which is more secure and a morden standard
    else:
        print('UNKNOWN DATABASE SELECTION:', selected_database)
# *****************************************************************************************************************************************

# initialize database *********************************************************************************************************************
def init_db():
    # connect to db *************************************************************************************************************
    # get the MongoDB client from the MongoEngine connection
    try:
        # client
        client = get_connection()
        # check if the connection is already established
        if client is None:
            print("No client connection available. Attempting to connect...")
            connect_to_database()
            print("New database connection established.")
        else:
            print("Client connection retrieved.")
            # if client is not None, check if it's primary
            if client.is_primary:
                print("Already connected to the primary database.")
            else:
                print("Connected to a secondary node.")
    except mongoengine.connection.ConnectionFailure as e:
        print(f'Connection failed: {e}')
        print('Establishing new database connection.')
        connect_to_database()
        print("New database connection established.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        connect_to_database()
    # ***************************************************************************************************************************
    # get all users *************************************************************************************************************
    users = Users.objects.all()
    # ***************************************************************************************************************************
# *****************************************************************************************************************************************

# close database connection ***************************************************************************************************************
def close_db():
    # disconnect from connection url
    disconnect()
# *****************************************************************************************************************************************