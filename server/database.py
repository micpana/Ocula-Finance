from models import Users
from mongoengine import connect
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

if selected_database == 'mock':
    # mock db connection
    connect('ocula-finance-test', host='mongomock://localhost', alias='default')
elif selected_database == 'test':
    # test db connection
    connect_url = 'mongodb://'+test_db_username+':'+test_db_password+'@localhost:27017/ocula-finance-test'
    connect(host=connection_url)
elif selected_database == 'live':
    # live db connection
    connect_url = 'mongodb+srv://'+live_db_username+':'+live_db_password+'@cluster0.6cicshr.mongodb.net/?retryWrites=true&w=majority'
    connect(host=connect_url, ssl=True, ssl_cert_reqs='CERT_NONE')
else:
    print('UNKNOWN DATABASE SELECTION:', selected_database)

def init_db():
    users = Users.objects.all()