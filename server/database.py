from models import  users
from mongoengine import connect
import dns
import urllib
from encrypt import encrypt_password, check_encrypted_password
from datetime import datetime

# connect('partify', host='mongomock://localhost', alias='default')
# connect('partify', host='localhost', port=27017, alias='default')
connect(host='mongodb+srv://admin:xfvrBsDncIFbED44@cluster0.6cicshr.mongodb.net/?retryWrites=true&w=majority', ssl=True, ssl_cert_reqs='CERT_NONE') # Live DB

def init_db():
    users = Users.objects.all()