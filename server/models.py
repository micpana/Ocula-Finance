from datetime import datetime
from mongoengine import Document, EmbeddedDocument
from mongoengine.fields import (
    DateTimeField, EmbeddedDocumentField,
    ListField, ReferenceField, StringField,
    ObjectIdField, IntField, BooleanField, FloatField
)

class Users(Document):
    meta = {'collection': 'users'}
    firstname = StringField(required=True) 
    lastname = StringField(required=True)
    username = StringField(required=True)
    email = StringField(required=True)
    phonenumber = StringField(required=True)
    password = StringField(required=True)
    country = StringField(required=True)
    date_of_registration = StringField(required=True)
    verified = BooleanField(required=True)
    subscription_date = StringField(required=False)
    subscription_expiry = StringField(required=False)
    role = StringField(required=True)
    role_issued_by = StringField(required=True)
    banned = BooleanField(required=True)
    banned_by = StringField(required=False)
    ban_reason = StringField(required=False)
    unbanned_by = StringField(required=False)
    ban_time = StringField(required=False)
    unban_time = StringField(required=False)

class EmailVerifications(Document):
    meta = {'collection': 'emailverifications'}
    account_id = StringField(required=True)
    email = StringField(required=True)
    purpose = StringField(required=True)
    used = BooleanField(required=True)
    device = StringField(required=True)
    ip_address = StringField(required=True)
    date_of_request = StringField(required=True)
    expiry_date = StringField(required=True)

class UserAccessTokens(Document):
    meta = {'collection': 'useraccesstokens'}
    user_id = StringField(required=True)
    token = StringField(required=True)
    active = BooleanField(required=True)
    signin_date = StringField(required=True)
    signout_date = StringField(required=False)
    user_browsing_agent = StringField(required=True)
    user_os = StringField(required=True)
    user_device = StringField(required=True)
    user_ip_address = StringField(required=True)
    user_browser = StringField(required=True)
    last_used_on_date = StringField(required=True)
    expiry_date = StringField(required=True)

class PasswordRecoveries(Document):
    meta = {'collection': 'passwordrecoveries'}
    account_id = StringField(required=True)
    email = StringField(required=True)
    used = BooleanField(required=True)
    device = StringField(required=True)
    ip_address = StringField(required=True)
    date_of_request = StringField(required=True)
    expiry_date = StringField(required=True)

class MarketAnalysis(Document):
    meta = {'collection': 'marketanalysis'}
    timestamp = StringField(required=True)
    entry_timeframe_last_timestamp = StringField(required=True)
    asset = StringField(required=True)
    maximum_possible_down_move = FloatField(required=True)
    maximum_possible_up_move = FloatField(required=True)

class Payments(Document):
    meta = {'collection': 'payments'}
    date = StringField(required=True)
    user_id = StringField(required=True)
    purpose = StringField(required=True)
    payment_method = StringField(required=True)
    transaction_id = StringField(required=True)
    verified = BooleanField(required=True)
    discount_supplied = FloatField(required=True)
    amount = FloatField(required=True)
    expiry_date = StringField(required=True)
    entered_by = StringField(required=True)

class LoginTrials(Document):
    meta = {'collection': 'logintrials'}
    account_id = StringField(required=True)
    email = StringField(required=True)
    device = StringField(required=True)
    os = StringField(required=True)
    browser = StringField(required=True)
    ip_address = StringField(required=True)
    date_and_time = StringField(required=True)
    successful = BooleanField(required=True)
    description = StringField(required=True)
