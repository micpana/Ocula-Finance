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
    subscribed = BooleanField(required=True)
    subscription_date = StringField(required=True)
    subscription_expiry = StringField(required=True)
    role = StringField(required=True)

class EmailVerifications(Document):
    meta = {'collection': 'emailverifications'}
    email = StringField(required=True)
    verification_token = StringField(required=True)
    used = BooleanField(required=True)
    device = StringField(required=True)
    ip_address = StringField(required=True)
    date_of_request = StringField(required=True)
    expiry_date = StringField(required=True)

class UserAccessTokens(Document):
    meta = {'collection': 'accesstokens'}
    user_id = StringField(required=True)
    active = BooleanField(required=True)
    signin_date = StringField(required=True)
    device = StringField(required=True)
    ip_address = StringField(required=True)
    last_used_on_date = StringField(required=True)
    expiry_date = StringField(required=True)

class PasswordRecoveries(Document):
    meta = {'collection': 'passwordrecoveries'}
    email = StringField(required=True)
    recovery_token = StringField(required=True)
    used = StringField(required=True)
    device = StringField(required=True)
    ip_address = StringField(required=True)
    date_of_request = StringField(required=True)
    expiry_date = StringField(required=True)

class MarketAnalysis(Document):
    meta = {'collection': 'marketanalysis'}
    timestamp = StringField(required=True)
    asset = StringField(required=True)
    maximum_possible_down_move = FloatField(required=True)
    maximum_possible_up_move = FloatField(required=True)
    market_overview_by_ai = StringField(required=True)
    news_ids = StringField(required=True)
    reports_ids = StringField(required=True)
    events_ids = StringField(required=True)

class NewsArticles(Document):
    meta = {'collection': 'newsarticles'}
    date_released = StringField(required=True)
    asset = StringField(required=True)
    source = StringField(required=True)
    url = StringField(required=True)
    title = StringField(required=True)
    date_acquired = StringField(required=True)

class UpcomingNewsEvents(Document):
    meta = {'collection': 'upcomingnewsevents'}
    date_released = StringField(required=True)
    asset = StringField(required=True)
    source = StringField(required=True)
    name = StringField(required=True)
    url = StringField(required=True)
    date_acquired = StringField(required=True)

class FinancialReports(Document):
    meta = {'collection': 'financialreports'}
    date_released = StringField(required=True)
    asset = StringField(required=True)
    source = StringField(required=True)
    url = StringField(required=True)
    title = StringField(required=True)
    date_acquired = StringField(required=True)

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