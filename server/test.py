from models import Users
from mongoengine import connect
from mongomock import MongoClient
from pytz import timezone
from datetime import datetime, timedelta

# connect to db
client = MongoClient(mongo_client_class=MongoClient, db_name="ocula-finance-test")
port = client.address[1]
print('Host:', client.address, '| Port:', port, '| Client Class:', MongoClient)
connect(host=f"localhost:{port}", mongo_client_class=MongoClient)

# add items to db
user_details = Users(
    firstname = 'Michael',
    lastname = 'Mudimbu',
    username = 'micpana',
    email = 'michaelmudimbu@gmail.com',
    phonenumber = '+263782464219',
    password = 'Testqwerty',
    country = 'Zimbabwe',
    date_of_registration = str(datetime.now(timezone('Africa/Harare'))),
    verified = False,
    subscription_date = '',
    subscription_expiry = '',
    role = 'user',
    role_issued_by = 'system',
    banned = False,
    banned_by = '',
    ban_reason = '',
    unbanned_by = '',
    ban_time = '',
    unban_time = ''
)
user_details.save()
account_id = str(user_details.id)
print('ID:', account_id)

# all items
all = Users.objects.all()
print('All:', all.to_json())

# query in db
user = Users.objects.filter(email = 'michaelmudimbu@gmail.com')

# update in db
user_id = str(user[0].id)
Users.objects(id = user_id).update(verified = True)
print('All after update:', Users.objects.all().to_json())

# delete in db
Users.objects(id = user_id).delete()
print('All after deletion:', Users.objects.all())