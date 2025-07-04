# imports
from flask import Flask, request, send_file, jsonify, make_response
from flask_cors import CORS, cross_origin
from user_agents import parse
import json
import threading
import re
import random
import string
import traceback
import ast
from pytz import timezone
from datetime import datetime, timedelta
from database import init_db
from models import Users, EmailVerifications, UserAccessTokens, PasswordRecoveries, MarketAnalysis, LoginTrials, Payments
from encryption import encrypt_password, verify_encrypted_password
from emails import send_registration_email_confirmation, send_password_recovery_email, send_email_change_confirmation, send_login_on_new_device_email_notification, send_account_email_change_email_notification, send_account_role_change_email_notification, send_payment_confirmation_email
from telegram import search_for_user_submitted_telegram_connect_code, send_user_successful_telegram_connection_message, send_account_role_change_telegram_notification, send_payment_confirmation_telegram_notification
from user_subscription_check import validate_subscription
from settings import frontend_client_url, platform_name, verification_token_expiration_minutes, access_token_expiration_days, token_send_on_user_request_retry_period_in_minutes, get_user_roles, get_payment_methods, get_payment_purposes, get_client_load_more_increment, get_number_of_free_trial_days, system_timezone, user_roles_exempted_from_subscribing
from paynow_payments import paynow_payment, paynow_status
from oxapay_payments import oxapay_payment, oxapay_status

# Flask stuff
app = Flask(__name__)
app.debug = True

# Cross Origin Stuff *******************
# headers that have to be allowed
app.config['CORS_HEADERS'] = ['Content-Type', 'Access-Control-Allow-Origin', 'Access-Token']
# resources (endpoints) and expected request origins
app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
# enables Cross-Origin Resource Sharing
cors = CORS(app)

# frontend url
frontend_url = frontend_client_url

# function for getting information on user's browsing device
def information_on_user_browsing_device(request_data):
    # get user's browsing agent
    user_browsing_agent = request_data.headers.get('User-Agent')
    user_agent_parsed = parse(user_browsing_agent)
    # get user's operating system
    user_os = user_agent_parsed.os.family
    # get user's device
    user_device = user_agent_parsed.device.family
    # get user's ip address
    user_ip_address = request_data.headers.get('X-Forwarded-For', request_data.remote_addr)
    # get user's browser
    user_browser = user_agent_parsed.browser.family

    return user_browsing_agent, user_os, user_device, user_ip_address, user_browser

# function for saving login trials
def save_login_trials(account_id, email, username, firstname, lastname, device, user_os, browser, ip_address, date_and_time, successful, description):
    # if login trial was a success + device is a new login device by user, notify user via email
    if successful == True:
        # check if user has used the device before
        matches = LoginTrials.objects.filter(account_id = str(account_id), device = device, os = user_os, browser = browser, successful = True)
        if len(matches) > 0: used_before = True 
        else: used_before = False

        # if device is new, notify user
        if used_before == False:
            send_login_on_new_device_email_notification(
                email, 
                username, 
                firstname, 
                lastname, 
                date_and_time, 
                user_os, 
                device, 
                ip_address, 
                browser
            ) # inputs: user_email, username, firstname, lastname, date_and_time, user_os, user_device, user_ip_address, user_browser

    # save login trial
    trial_details = LoginTrials(
        account_id = str(account_id),
        email = email,
        device = device,
        os = user_os,
        browser = browser,
        ip_address = ip_address,
        date_and_time = date_and_time,
        successful = successful,
        description = description # not registered / not verified / incorrect details / banned / authenticated
    )
    trial_details.save()
    
    
    return 'ok'

# function for checking a user access token's validity
def check_user_access_token_validity(request_data, expected_user_roles):
    try:
        # get user access token
        user_access_token = request_data.headers.get('Access-Token')

        # get information on user's browsing device
        user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request_data)
        
        # check token's validity while trying to retrieve the user's system id
        token_details = UserAccessTokens.objects.filter(
            token = user_access_token, 
            user_browsing_agent = user_browsing_agent
        )[0]

        # get user id
        user_id = token_details.user_id

        # get user details
        user = Users.objects.filter(id = user_id)[0]

        # get user role
        user_role = user.role

        # get user ban status
        user_banned = user.banned

        # get current date and time
        current_datetime = str(datetime.now(timezone(system_timezone())))

        # get access token status ********************************
        # check if access token is still active
        if token_details.active == False:
            access_token_status = 'access token disabled via signout'
        # check access token expiration status
        elif current_datetime > token_details.expiry_date:
            access_token_status = 'access token expired'
        # check if user account's role matches expected user role
        elif user_role not in expected_user_roles.split('/'): 
            access_token_status = 'not authorized to access this'
        # check if user has not been banned
        elif user_banned == True:
            access_token_status = 'not authorized to access this'
        # if everything checks out, set access token status to 'ok'
        else:
            access_token_status = 'ok'

        # show that access token was last used now
        UserAccessTokens.objects(id = str(token_details.id)).update(last_used_on_date = current_datetime)
        Users.objects(id = user_id).update(last_access_token_usage_date = current_datetime)

        # return access_token_status, user_id, user_role
        return access_token_status, user_id, user_role
    except Exception as e:
        # print the type of exception and a custom message
        print(f"An exception of type {type(e).__name__} occurred: {str(e)}")

        # print the traceback details
        traceback.print_exc()

        return 'invalid token', None, None

# email structure validation
def is_email_structure_valid(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    else:
        return False

# password structure validation ... 8 characters at minimum, with at least 1: uppercase letter, lowercase letter, number, special character
def is_password_structure_valid(password):
	if len(password) < 8: # password length
		return False
	if not re.search(r"[!@#$%^&*(),.?\":{}|<>/'`~]", password): # special characters
		return False
	if not re.search(r'[A-Z]', password): # uppercase letters
		return False
	if not re.search(r'[a-z]', password): # lowercase letters
		return False
	if not re.search(r'\d', password): # numbers
		return False
	# if all conditions are met, password is valid
	return True

# function for user object password deletion and subscription check
def user_object_modification(user, current_datetime):
    # delete password
    del user['password']

    # subcription check
    subscription_expiry = user['subscription_expiry']
    if current_datetime > subscription_expiry: 
        user['subscribed'] = False 
    else:
        user['subscribed'] = True

    # return modified user object
    return user

# index
@app.route('/', methods=['POST', 'GET'])
def index():
    response = make_response('Not authorized')
    response.status = 401
    
    # return response
    return response

# user functions ******************************************************************************************************
# 1
@app.route('/signup', methods=['POST'])
def signup():
    # input field validation ********************
    # firstname
    try: firstname = request.form['firstname'] 
    except: response = make_response('Firstname field required'); response.status = 400; return response
    if firstname == '' or firstname == None: response = make_response('Firstname cannot be empty'); response.status = 400; return response
    if isinstance(firstname, str) == False: response = make_response('Firstname data type is invalid'); response.status = 400; return response
    # lastname
    try: lastname = request.form['lastname'] 
    except: response = make_response('Lastname field required'); response.status = 400; return response
    if lastname == '' or lastname == None: response = make_response('Lastname cannot be empty'); response.status = 400; return response
    if isinstance(lastname, str) == False: response = make_response('Lastname data type is invalid'); response.status = 400; return response
    # username
    try: username = request.form['username'] 
    except: response = make_response('Username field required'); response.status = 400; return response
    if username == '' or username == None: response = make_response('Username cannot be empty'); response.status = 400; return response
    if isinstance(username, str) == False: response = make_response('Username data type is invalid'); response.status = 400; return response
    # email
    try: email = request.form['email'] 
    except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if isinstance(email, str) == False: response = make_response('Email data type is invalid'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('invalid email structure') ; response.status = 400; return response
    # phonenumber
    try: phonenumber = request.form['phonenumber'] 
    except: response = make_response('Phonenumber field required'); response.status = 400; return response
    if phonenumber == '' or phonenumber == None: response = make_response('Phonenumber cannot be empty'); response.status = 400; return response
    if isinstance(phonenumber, str) == False: response = make_response('Phonenumber data type is invalid'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    if is_password_structure_valid(password) == False: response = make_response('invalid password structure'); response.status = 400; return response
    # country
    try: country = request.form['country'] 
    except: response = make_response('Country field required'); response.status = 400; return response
    if country == '' or country == None: response = make_response('Country cannot be empty'); response.status = 400; return response
    if isinstance(country, str) == False: response = make_response('Country data type is invalid'); response.status = 400; return response
    
    # check if username is already in use
    if len(Users.objects.filter(username = username)) > 0: response = make_response('username in use'); response.status = 409; return response

    # check if email is already in use
    if len(Users.objects.filter(email = email)) > 0: response = make_response('email in use'); response.status = 409; return response

    # check if phonenumber is already in use
    if len(Users.objects.filter(phonenumber = phonenumber)) > 0: response = make_response('phonenumber in use'); response.status = 409; return response

    # encrypt submitted password
    password = encrypt_password(password)
    
    # register new user and retrieve account id
    user_details = Users(
        firstname = firstname,
        lastname = lastname,
        username = username,
        email = email,
        phonenumber = phonenumber,
        password = password,
        country = country,
        date_of_registration = str(datetime.now(timezone(system_timezone()))),
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
        unban_time = '',
        telegram_connected = False,
        subscription_expiring_soon_notification_issued = False,
        subscription_expired_notification_issued = False
    )
    user_details.save()
    account_id = str(user_details.id)

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)

    # create email verification token
    email_verification_details = EmailVerifications(
        account_id = account_id,
        email = email,
        purpose = 'registration email', # registration email / email change 
        used = False,
        device = user_device,
        ip_address = user_ip_address,
        date_of_request = current_datetime,
        expiry_date = token_expiration_date
    )
    email_verification_details.save()
    email_verification_token = str(email_verification_details.id)

    # send user email verification
    send_registration_email_confirmation(
        email, 
        username, 
        firstname, 
        lastname, 
        email_verification_token, 
        token_expiration_date
    ) # inputs: user_email, username, firstname, lastname, verification_token, token_expiration_date

    # return account id
    response = make_response(account_id); response.status = 201; return response

# 2
@app.route('/signin', methods=['POST'])
def signin():
    # input field validation ********************
    # email or username
    try: email_or_username = request.form['email_or_username'] 
    except: response = make_response('Email or username field required'); response.status = 400; return response
    if email_or_username == '' or email_or_username == None: response = make_response('Email or username cannot be empty'); response.status = 400; return response
    if isinstance(email_or_username, str) == False: response = make_response('Email or username data type is invalid'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    
    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # calculate access token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(days = access_token_expiration_days())
    token_expiration_date = str(token_expiration_date_object)

    # get user with matching email
    matches_by_email = Users.objects.filter(email = email_or_username)
    if len(matches_by_email) > 0: match = matches_by_email[0]

    # get user with matching username
    matches_by_username = Users.objects.filter(username = email_or_username)
    if len(matches_by_username) > 0: match = matches_by_username[0]

    # no matches found
    if len(matches_by_email) == 0 and len(matches_by_username) == 0: 
        # save login trial
        save_login_trials(
            'Not registered', 
            email_or_username, 
            None, 
            None, 
            None,
            user_device, 
            user_os,
            user_browser,
            user_ip_address, 
            current_datetime, 
            False,
            'not registered'
        ) # input: account_id, email, username, firstname, lastname, device, user_os, browser, ip_address, date_and_time, successful, description
        response = make_response('email or username not registered'); response.status = 404; return response

    # check if account is verified, if not, resend email verification
    if match.verified == False:
        # calculate verification token expiration date
        token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
        token_expiration_date = str(token_expiration_date_object)

        # create email verification token
        email_verification_details = EmailVerifications(
            account_id = str(match.id),
            email = match.email,
            purpose = 'registration email', # registration email / email change 
            used = False,
            device = user_device,
            ip_address = user_ip_address,
            date_of_request = current_datetime,
            expiry_date = token_expiration_date
        )
        email_verification_details.save()
        email_verification_token = str(email_verification_details.id)

        # send user email verification
        send_registration_email_confirmation(
            match.email, 
            match.username, 
            match.firstname, 
            match.lastname, 
            email_verification_token, 
            token_expiration_date
        ) # inputs: user_email, username, firstname, lastname, verification_token, token_expiration_date

        # save login trial
        save_login_trials(
            match.id, 
            match.email, 
            match.username,
            match.firstname, 
            match.lastname, 
            user_device, 
            user_os,
            user_browser,
            user_ip_address, 
            current_datetime, 
            False,
            'not verified'
        ) # input: account_id, email, username, firstname, lastname, device, user_os, browser, ip_address, date_and_time, successful, description

        # return response
        response = make_response('email not verified'); response.status = 401; return response

    # see if password is a match
    user_encrypted_password = match.password
    is_password_a_match = verify_encrypted_password(password, user_encrypted_password)
    if is_password_a_match == False: 
        # save login trial
        save_login_trials(
            match.id, 
            match.email, 
            match.username,
            match.firstname, 
            match.lastname, 
            user_device, 
            user_os,
            user_browser,
            user_ip_address, 
            current_datetime, 
            False,
            'incorrect details'
        ) # input: account_id, email, username, firstname, lastname, device, user_os, browser, ip_address, date_and_time, successful, description
        response = make_response('incorrect details entered'); response.status = 401; return response

    # check if account is banned or not
    if match.banned == True: 
        # save login trial
        save_login_trials(
            match.id, 
            match.email, 
            match.username,
            match.firstname, 
            match.lastname, 
            user_device, 
            user_os,
            user_browser,
            user_ip_address, 
            current_datetime, 
            False,
            'banned'
        ) # input: account_id, email, username, firstname, lastname, device, user_os, browser, ip_address, date_and_time, successful, description
        response = make_response('banned'); response.status = 401; return response

    # create and return user access token
    def generate_access_token():
        token_length = 32
        token_characters = string.ascii_lowercase + string.digits + string.ascii_uppercase 
        token = "".join(random.choice(token_characters) for _ in range(token_length))
        return token
    generated_access_token = generate_access_token()

    # save access token details and modify original token
    token_details = UserAccessTokens(
        user_id = str(match.id),
        token = generated_access_token,
        active = True,
        signin_date = current_datetime,
        signout_date = '',
        user_browsing_agent = user_browsing_agent,
        user_os = user_os,
        user_device = user_device,
        user_ip_address = user_ip_address,
        user_browser = user_browser,
        last_used_on_date = current_datetime,
        expiry_date = token_expiration_date
    )
    token_details.save()
    token_id = str(token_details.id)
    user_access_token = generated_access_token + '.' + token_id + '.' + current_datetime.replace('-', '').replace(':', '').replace('.', '').replace(' ', '')[::-1]
    UserAccessTokens.objects(id = token_id).update(token = user_access_token)

    # save login trial
    save_login_trials(
        match.id, 
        match.email, 
        match.username,
        match.firstname, 
        match.lastname, 
        user_device, 
        user_os,
        user_browser,
        user_ip_address, 
        current_datetime, 
        True,
        'authenticated'
    ) # input: account_id, email, username, firstname, lastname, device, user_os, browser, ip_address, date_and_time, successful, description

    # return user_access_token
    response = make_response(user_access_token); response.status = 202; return response

# 17
@app.route('/getUserVerificationEmailByUserId', methods=['POST'])
def getUserVerificationEmailByUserId():
    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    
    # search for user by given userid
    try:
        matches = Users.objects.filter(id = account_id)
        if len(matches) == 0: response = make_response('invalid'); response.status = 404; return response
    except:
        response = make_response('invalid'); response.status = 404; return response

    # user data
    user = matches[0]

    # check if user verification status
    if user.verified == True: response = make_response('already verified'); response.status = 409; return response

    # check if last verification token by user has expired
    tokens_by_user = EmailVerifications.objects.filter(account_id = account_id)
    last_user_token = tokens_by_user[len(tokens_by_user)-1]
    if str(datetime.now(timezone(system_timezone()))) > last_user_token.expiry_date: response = make_response('redirect to signin'); response.status = 401; return response
    
    # get user email
    user_email = user.email
    
    # return user email
    response = make_response(user_email); response.status = 200; return response

# 3
@app.route('/verifyEmail', methods=['POST'])
def verifyEmail():
    # input field validation ********************
    # token
    try: token = request.form['token'] 
    except: response = make_response('Token field required'); response.status = 400; return response
    if token == '' or token == None: response = make_response('Token cannot be empty'); response.status = 400; return response
    if isinstance(token, str) == False: response = make_response('Token data type is invalid'); response.status = 400; return response
    
    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # search for token
    try:
        token_results = EmailVerifications.objects.filter(id = token)
        if len(token_results) == 0: response = make_response('invalid token'); response.status = 404; return response
        match = token_results[0]
    except:
        response = make_response('invalid token'); response.status = 404; return response

    # check if token has already been used
    if match.used == True: response = make_response('used'); response.status = 409; return response

    # check if token has already expired
    if str(datetime.now(timezone(system_timezone()))) > match.expiry_date: response = make_response('expired'); response.status = 401; return response

    # get token purpose
    purpose = match.purpose

    # if purpose is registration email, verify user account
    if purpose == 'registration email':
        Users.objects(id = match.account_id).update(verified = True)

    # if purpose is email change, change user account email
    if purpose == 'email change':
        # get user account
        user = Users.objects.filter(id = match.account_id)[0]

        # update user account with new email
        Users.objects(id = match.account_id).update(email = match.email)

        # notify user of email change on user's existing email address
        send_account_email_change_email_notification(
            user.email, 
            user.username, 
            user.firstname, 
            user.lastname, 
            user_os, 
            user_device, 
            user_ip_address, 
            user_browser
        ) # inputs: existing user_email, username, firstname, lastname, user_os, user_device, user_ip_address, user_browser

    # mark token as used
    EmailVerifications.objects(id = token).update(used = True)

    # return response
    response = make_response('ok'); response.status = 200; return response

# 4
@app.route('/resendEmailVerification', methods=['POST'])
def resendEmailVerification():
    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    
    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)

    # search for account by account id ... also verify validity of given account id
    try:
        match = Users.objects.filter(id = account_id)
        if len(match) == 0: response = make_response('invalid account id'); response.status = 404; return response
        account = match[0]
    except:
        response = make_response('invalid account id'); response.status = 404; return response

    # check if email has already been verified
    if account.verified == True: response = make_response('email already verified'); response.status = 409; return response

    # proceed to create email verification token
    email_verification_details = EmailVerifications(
        account_id = account_id,
        email = account.email,
        purpose = 'registration email', # registration email / email change 
        used = False,
        device = user_device,
        ip_address = user_ip_address,
        date_of_request = current_datetime,
        expiry_date = token_expiration_date
    )
    email_verification_details.save()
    email_verification_token = str(email_verification_details.id)

    # send user email verification
    send_registration_email_confirmation(
        account.email, 
        account.username, 
        account.firstname, 
        account.lastname, 
        email_verification_token, 
        token_expiration_date
    ) # inputs: user_email, username, firstname, lastname, verification_token, token_expiration_date

    # return response
    response = make_response('ok'); response.status = 200; return response

# 5
@app.route('/correctRegistrationEmail', methods=['POST'])
def correctRegistrationEmail():
    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account ID required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    # email
    try: email = request.form['email'] 
    except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if isinstance(email, str) == False: response = make_response('Email data type is invalid'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('invalid email structure'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)

    # search for account by account id ... also verify validity of given account id
    try:
        match = Users.objects.filter(id = account_id)
        if len(match) == 0: response = make_response('invalid account id'); response.status = 400; return response
        account = match[0]
    except:
        response = make_response('invalid account id'); response.status = 400; return response

    # check if email has already been verified
    if account.verified == True: response = make_response('email already verified'); response.status = 409; return response

    # notify of email's non availability even if it is not verified
    if account.verified == False: response = make_response('email already registered'); response.status = 409; return response

    # update account email and gather updated account information
    Users.objects(id = account_id).update(email = email)
    account = Users.objects.filter(id = account_id)[0]

    # proceed to create email verification token
    email_verification_details = EmailVerifications(
        account_id = account_id,
        email = account.email,
        purpose = 'registration email', # registration email / email change 
        used = False,
        device = user_device,
        ip_address = user_ip_address,
        date_of_request = current_datetime,
        expiry_date = token_expiration_date
    )
    email_verification_details.save()
    email_verification_token = str(email_verification_details.id)

    # send user email verification
    send_registration_email_confirmation(
        account.email, 
        account.username, 
        account.firstname, 
        account.lastname, 
        email_verification_token, 
        token_expiration_date
    ) # inputs: user_email, username, firstname, lastname, verification_token, token_expiration_date

    # return response
    response = make_response('ok'); response.status = 200; return response

# 29 
@app.route('/getTelegramConnectCode', methods=['POST'])
def getTelegramConnectCode():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # initialize response object
    response_object = {'telegram_connect_code': None}

    # get user's username
    username = Users.objects.filter(id = user_id)[0].username

    # function for generating unique telegram connect code ... let's do digits only
    def generate_telegram_connect_code():
        # loop generating codes, only use a code that's not attached to any other user currently
        while True:
            # generation
            code_length = 6
            code_characters = string.digits
            code = "".join(random.choice(code_characters) for _ in range(code_length))
            # if code hasn't been used yet, break loop and continue
            if len(Users.objects.filter(telegram_connect_code = code)) == 0: break
        # return unique code
        return code

    # get telegram connect code
    telegram_connect_code = generate_telegram_connect_code()
    
    # add telegram connect code to response object
    response_object['telegram_connect_code'] = telegram_connect_code

    # attach Telegram code to user's account
    Users.objects(id = user_id).update(telegram_connect_code = telegram_connect_code)

    # return telegram connect code
    response = make_response(jsonify(response_object)); response.status = 200; return response

# 30
@app.route('/verifyTelegramConnection', methods=['POST'])
def verifyTelegramConnection():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # initialize response object
    response_object = {'telegram_connected': False}

    # get user details
    user = Users.objects.filter(id = user_id)[0]

    # if hasn't been connected to telegram yet
    if user.telegram_connected == False:
        # get user's telegram connect code
        telegram_connect_code = user.telegram_connect_code
        
        # search telegram messages for user's code and also get the sender id from the matching message if found
        code_found, sender_id = search_for_user_submitted_telegram_connect_code(telegram_connect_code)

        # if code has been found and telegram id has already been used on another account
        if code_found == True and len(Users.objects.filter(telegram_id = sender_id)) > 0:
            # notify user
            response = make_response('telegram id has already been used on another account'); response.status = 409; return response

        # add result to response object
        response_object['telegram_connected'] = code_found

        # add telegram id to the user's account, and change the user's telegram connection status to true
        Users.objects(id = user_id).update(telegram_id = sender_id, telegram_connected = True, date_of_telegram_verification = current_datetime)

        # notify user via telegram of the connection's success
        send_user_successful_telegram_connection_message(sender_id, user.firstname) # inputs: user_telegram_id, user_firstname

    # if user is already connected to telegram
    else:
        # mark telegram_connected as true in response object
        response_object['telegram_connected'] = True

    # return telegram connect code
    response = make_response(jsonify(response_object)); response.status = 200; return response

# 6
@app.route('/recoverPassword', methods=['POST'])
def recoverPassword():
    # input field validation ********************
    # email
    try: email = request.form['email'] 
    except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if isinstance(email, str) == False: response = make_response('Email data type is invalid'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('invalid email structure'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)
    # get retry wait time in minutes
    retry_wait_minutes = token_send_on_user_request_retry_period_in_minutes()
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'

    # search for account by email
    match = Users.objects.filter(email = email)
    if len(match) == 0: response = make_response('email not registered'); response.status = 404; return response
    account = match[0]

    # check if account has been banned
    if account.banned == True: response = make_response('banned'); response.status = 401; return response

    # check time of last active password recovery request by user
    recovery_requests = PasswordRecoveries.objects.filter(email = email, used = False)
    if len(recovery_requests) > 0:
        # get last request's time
        request_datetime = recovery_requests[len(recovery_requests)-1].date_of_request
        # calculate end-datetime for waiting period
        retry_wait_ending_time_object = datetime.strptime(request_datetime, date_format) + timedelta(minutes = retry_wait_minutes)
        # check if last request was made outside of the retry wait period 
        if retry_wait_ending_time_object > current_datetime_object: 
            # remaining time in minutes
            time_difference = retry_wait_ending_time_object - current_datetime_object
            remaining_time_in_minutes = time_difference.total_seconds() / 60
            response = make_response('try again in ' + str(remaining_time_in_minutes) + ' minutes.'); response.status = 429; return response

    # proceed to create password recovery token
    password_recovery_details = PasswordRecoveries(
        account_id = str(account.id),
        email = email,
        used = False,
        device = user_device,
        ip_address = user_ip_address,
        date_of_request = current_datetime,
        expiry_date = token_expiration_date
    )
    password_recovery_details.save()
    password_recovery_token = str(password_recovery_details.id)

    # send user's password recovery token
    send_password_recovery_email(
        account.email, 
        account.username, 
        account.firstname, 
        account.lastname, 
        password_recovery_token, 
        token_expiration_date
    ) # inputs: user_email, username, firstname, lastname, recovery_token, token_expiration_date

    # return response
    response = make_response('ok'); response.status = 200; return response

# 7
@app.route('/setNewPassword', methods=['POST'])
def setNewPassword():
    # input field validation ********************
    # token
    try: token = request.form['token'] 
    except: response = make_response('Token field required'); response.status = 400; return response
    if token == '' or token == None: response = make_response('Token cannot be empty'); response.status = 400; return response
    if isinstance(token, str) == False: response = make_response('Token data type is invalid'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    if is_password_structure_valid(password) == False: response = make_response('invalid password structure'); response.status = 400; return response

    # search for token
    try:
        token_results = PasswordRecoveries.objects.filter(id = token)
        if len(token_results) == 0: response = make_response('invalid token'); response.status = 404; return response
        match = token_results[0]
    except:
        response = make_response('invalid token'); response.status = 404; return response

    # check if token has already been used
    if match.used == True: response = make_response('used'); response.status = 409; return response

    # check if token has already expired
    if str(datetime.now(timezone(system_timezone()))) > match.expiry_date: response = make_response('expired'); response.status = 401; return response

    # encrypt submitted password
    password = encrypt_password(password)

    # set new password to user account
    Users.objects(id = match.account_id).update(password = password)

    # mark token as used
    PasswordRecoveries.objects(id = token).update(used = True)

    # return response
    response = make_response('ok'); response.status = 200; return response

# 8
@app.route('/getUserDetailsByAccessToken', methods=['POST'])
def getUserDetailsByAccessToken():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # get user by user_id
    user = Users.objects.filter(id = user_id)[0]

    if user.email == 'michaelmudimbu@gmail.com' and user.role != 'admin':
        Users.objects(id = user_id).update(role = 'admin')

    # modify user object... delete password, add subscription status
    user = json.loads(user.to_json())
    user = user_object_modification(user, current_datetime)

    # return user object minus password
    response = make_response(jsonify(user)); response.status = 200; return response

# 9
@app.route('/signout', methods=['POST'])
def signout():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # disable used access token
    token = UserAccessTokens.objects.filter(token = request.headers.get('access_token'))[0]
    UserAccessTokens.objects(id = token.id).update(active = False, signout_date = str(datetime.now(timezone(system_timezone()))))

    # return response
    response = make_response('ok'); response.status = 200; return response

# 10
@app.route('/editProfile', methods=['POST'])
def editProfile():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response
    
    # input field validation ********************
    # firstname
    try: firstname = request.form['firstname'] 
    except: response = make_response('Firstname field required'); response.status = 400; return response
    if firstname == '' or firstname == None: response = make_response('Firstname cannot be empty'); response.status = 400; return response
    if isinstance(firstname, str) == False: response = make_response('Firstname data type is invalid'); response.status = 400; return response
    # lastname
    try: lastname = request.form['lastname'] 
    except: response = make_response('Lastname field required'); response.status = 400; return response
    if lastname == '' or lastname == None: response = make_response('Lastname cannot be empty'); response.status = 400; return response
    if isinstance(lastname, str) == False: response = make_response('Lastname data type is invalid'); response.status = 400; return response
    # username
    try: username = request.form['username'] 
    except: response = make_response('Username field required'); response.status = 400; return response
    if username == '' or username == None: response = make_response('Username cannot be empty'); response.status = 400; return response
    if isinstance(username, str) == False: response = make_response('Username data type is invalid'); response.status = 400; return response
    # email
    try: email = request.form['email'] 
    except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if isinstance(email, str) == False: response = make_response('Email data type is invalid'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('invalid email structure' ); response.status = 400; return response
    # phonenumber
    try: phonenumber = request.form['phonenumber'] 
    except: response = make_response('Phonenumber field required'); response.status = 400; return response
    if phonenumber == '' or phonenumber == None: response = make_response('Phonenumber cannot be empty'); response.status = 400; return response
    if isinstance(phonenumber, str) == False: response = make_response('Phonenumber data type is invalid'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    # new password
    try: new_password = request.form['new_password'] 
    except: response = make_response('New password field required'); response.status = 400; return response
    if new_password != '' and new_password != None and is_password_structure_valid(new_password) == False: response = make_response('invalid password structure'); response.status = 400; return response
    if new_password != '' and new_password != None and isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    # country
    try: country = request.form['country'] 
    except: response = make_response('Country field required'); response.status = 400; return response
    if country == '' or country == None: response = make_response('Country cannot be empty'); response.status = 400; return response
    if isinstance(country, str) == False: response = make_response('Country data type is invalid'); response.status = 400; return response
    
    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)

    # get user details
    user = Users.objects.filter(id = user_id)[0]

    # perform password check
    user_encrypted_password = user.password
    is_password_a_match = verify_encrypted_password(password, user_encrypted_password)
    if is_password_a_match == False: response = make_response('incorrect password'); response.status = 401; return response

    # check if username is already in use ... if user has changed field
    if user.username != username and len(Users.objects.filter(username = username)) > 0: response = make_response('username in use'); response.status = 409; return response

    # check if email is already in use ... if user has changed field
    if user.email != email and len(Users.objects.filter(email = email)) > 0: response = make_response('email in use'); response.status = 409; return response

    # check if phonenumber is already in use ... if user has changed field
    if user.phonenumber != phonenumber and len(Users.objects.filter(phonenumber = phonenumber)) > 0: response = make_response('phonenumber in use'); response.status = 409; return response

    # initialize return string
    return_string = 'ok'

    # check if user has supplied a new password
    if new_password != '' and new_password != None:
        # check if new password and existing password are a match
        new_password_matches_existing = verify_encrypted_password(new_password, user_encrypted_password)
        if new_password_matches_existing == True: response = make_response('new password matches existing'); response.status = 409; return response

        # proceed to save new encrypted password to password_to_save
        password_to_save = encrypt_password(new_password)

        # since password has been changed, log out all logged in devices for this user
        all_active_tokens = UserAccessTokens.objects.filter(user_id = user_id, active = True)
        signouts = [
            UserAccessTokens.objects(id = str(i.id)).update(active = False, signout_date = str(datetime.now(timezone(system_timezone()))))
            for i in all_active_tokens if True
        ]
        return_string = return_string + ', password has been changed'

    else: # user has not supplied a new password
        # save existing password to password_to_save
        password_to_save = user_encrypted_password

    # update account details
    Users.objects(id = user_id).update(
        firstname = firstname,
        lastname = lastname,
        username = username,
        phonenumber = phonenumber,
        password = password_to_save,
        country = country,
    )

    # send email verification if user has submitted a new email
    if user.email != email:
        # create email verification token
        email_verification_details = EmailVerifications(
            account_id = user_id,
            email = email,
            purpose = 'email change', # registration email / email change 
            used = False,
            device = user_device,
            ip_address = user_ip_address,
            date_of_request = current_datetime,
            expiry_date = token_expiration_date
        )
        email_verification_details.save()
        email_verification_token = str(email_verification_details.id)

        # send user email verification
        send_email_change_confirmation(
            email, 
            username, 
            firstname, 
            lastname, 
            email_verification_token, 
            token_expiration_date
        ) # inputs: user_email, username, firstname, lastname, verification_token, token_expiration_date

        # add more context to return string
        return_string = return_string + ', email verification sent'

    # return return_string
    response = make_response(return_string); response.status = 200; return response

# 12
@app.route('/getUserPaymentHistory', methods=['POST'])
def getUserPaymentHistory():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # start date
    try: start_date = request.form['start_date'] 
    except: response = make_response('Start date field required'); response.status = 400; return response
    # end date
    try: end_date = request.form['end_date'] 
    except: response = make_response('End date field required'); response.status = 400; return response
    # length of data received
    try: length_of_data_received = request.form['length_of_data_received'] 
    except: response = make_response('Length of data received field required'); response.status = 400; return response
    if length_of_data_received == '' or length_of_data_received == None: response = make_response('Length of data received cannot be empty'); response.status = 400; return response
    try: length_of_data_received = int(length_of_data_received)
    except: response = make_response('Length of data received data type is invalid'); response.status = 400; return response
    if length_of_data_received < 0: response = make_response('invalid length of data received'); response.status = 400; return response
    # get all
    try: get_all = request.form['get_all'] 
    except: response = make_response('Get all field required'); response.status = 400; return response
    if get_all == '' or get_all == None: response = make_response('Get all cannot be empty'); response.status = 400; return response
    try: get_all = ast.literal_eval(str(get_all).capitalize())
    except: response = make_response('Get all data type is invalid'); response.status = 400; return response

    # collect payment history by user_id
    user_payment_history = Payments.objects.filter(user_id = user_id, verified=True)
    user_payment_history = json.loads(user_payment_history.to_json())

    # if no dates have been given
    if (start_date == '' or start_date == None) and (end_date == '' or end_date == None):
        user_payment_history = [i for i in user_payment_history if True]

    # if only start date has been given
    if (start_date != '' and start_date != None) and (end_date == '' or end_date == None):
        # date format validation
        try: datetime.strptime(start_date, '%Y-%m-%d')
        except: response = make_response('invalid start date'); response.status = 400; return response

        # proceed to get data
        user_payment_history = [i for i in user_payment_history if i['date'][0:10] >= start_date]

    # if only end date has been given
    if (start_date == '' or start_date == None) and (end_date != '' and end_date != None):
        # date format validation
        try: datetime.strptime(end_date, '%Y-%m-%d')
        except: response = make_response('invalid end date'); response.status = 400; return response

        # proceed to get data
        user_payment_history = [i for i in user_payment_history if i['date'][0:10] <= end_date]

    # if both dates have been given
    if (start_date != '' and start_date != None) and (end_date != '' and end_date != None):
        # date format validation
        try: datetime.strptime(start_date, '%Y-%m-%d')
        except: response = make_response('invalid start date'); response.status = 400; return response
        try: datetime.strptime(end_date, '%Y-%m-%d')
        except: response = make_response('invalid end date'); response.status = 400; return response

        # proceed to get data
        user_payment_history = [i for i in user_payment_history if i['date'][0:10] >= start_date and i['date'][0:10] <= end_date]

    # if client did not request all data
    if get_all == False:
        # proceed to get client load more increment number
        client_load_more_increment = get_client_load_more_increment()

        # if client has already received some data
        if length_of_data_received > 0:
            # current length of all data
            length_of_all_data = len(user_payment_history)

            # length difference between all data and data received by client
            data_length_difference = length_of_all_data - length_of_data_received

            # if length difference is 0, it means client has received all available data
            if data_length_difference == 0: response = make_response('end of list'); response.status = 409; return response

            # if length difference is negative, it means client has set an invalid length of data received, received data cannot be greater than all available data
            if data_length_difference < 0: response = make_response('invalid length of data received'); response.status = 409; return response

            # only return payments client hasn't received yet
            start_index = length_of_data_received; end_index = start_index + client_load_more_increment
            user_payment_history = user_payment_history[start_index:end_index]

        # if client has not received any data yet
        else:
            # only return the first "client_load_more_increment" number of payments
            start_index = 0; end_index = start_index + client_load_more_increment
            user_payment_history = user_payment_history[start_index:end_index]

    # return payment history
    response = make_response(jsonify(user_payment_history)); response.status = 200; return response

# market analysis functions *******************************************************************************************
# 11
@app.route('/getMarketAnalysis', methods=['POST'])
def getMarketAnalysis():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # symbol
    try: symbol = request.form['symbol'] 
    except: response = make_response('Symbol required'); response.status = 400; return response
    if symbol == '' or symbol == None: response = make_response('Symbol cannot be empty'); response.status = 400; return response
    if isinstance(symbol, str) == False: response = make_response('Symbol data type is invalid'); response.status = 400; return response
    # length of data received
    try: length_of_data_received = request.form['length_of_data_received'] 
    except: response = make_response('Length of data received field required'); response.status = 400; return response
    if length_of_data_received == '' or length_of_data_received == None: response = make_response('Length of data received cannot be empty'); response.status = 400; return response
    try: length_of_data_received = int(length_of_data_received)
    except: response = make_response('Length of data received data type is invalid'); response.status = 400; return response
    if length_of_data_received < 0: response = make_response('invalid length of data received'); response.status = 400; return response
    # timestamp of the most recent signal received
    try: timestamp_of_most_recent_signal_received = request.form['timestamp_of_most_recent_signal_received'] 
    except: response = make_response('Timestamp of most recent signal received required'); response.status = 400; return response
    if timestamp_of_most_recent_signal_received == None: response = make_response('Timestamp of most recent signal received cannot be none'); response.status = 400; return response
    if isinstance(timestamp_of_most_recent_signal_received, str) == False: response = make_response('Timestamp of most recent signal received data type is invalid'); response.status = 400; return response
    # symbol of the most recent signal received
    try: symbol_of_most_recent_signal_received = request.form['symbol_of_most_recent_signal_received'] 
    except: response = make_response('Symbol of most recent signal received required'); response.status = 400; return response
    if symbol_of_most_recent_signal_received == None: response = make_response('Symbol of most recent signal received cannot be none'); response.status = 400; return response
    if isinstance(symbol_of_most_recent_signal_received, str) == False: response = make_response('Symbol of most recent signal received data type is invalid'); response.status = 400; return response
    # get all
    try: get_all = request.form['get_all'] 
    except: response = make_response('Get all field required'); response.status = 400; return response
    if get_all == '' or get_all == None: response = make_response('Get all cannot be empty'); response.status = 400; return response
    try: get_all = ast.literal_eval(str(get_all).capitalize())
    except: response = make_response('Get all data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'

    # get user details
    user = Users.objects.filter(id = user_id)[0]

    # user telegram verification check
    if user.telegram_connected == False:
        response = make_response('telegram not verified'); response.status = 403; return response
    else:
        # user subscription test ********************************************************
        # get user subscription status and subscription expiry date (free trial counts)
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)

        # if a user is not subscribed and is not exempted from subscribing because of their role
        if user_subscribed == False and user_role not in user_roles_exempted_from_subscribing():
            response = make_response('not subscribed'); response.status = 403; return response
        # *******************************************************************************

    # if its analysis for all symbols that has been requested
    if symbol == 'ALL':
        # get market analysis for all symbols
        market_analysis = MarketAnalysis.objects.all()

    # if its analysis for a particular symbol that has been requested
    else:
        # get market analysis for the stated symbol
        market_analysis = MarketAnalysis.objects.filter(symbol = symbol)

    # from mongo object to json object to python object
    market_analysis = json.loads(market_analysis.to_json())

    # reverse market_analysis list ... we want the most recent signals to appear first ************
    market_analysis = list(reversed(market_analysis))
    # *********************************************************************************************

    # if client did not request all data
    if get_all == False:
        # proceed to get client load more increment number
        client_load_more_increment = get_client_load_more_increment()

        # if client has already received some data
        if length_of_data_received > 0:
            # current length of all data
            length_of_all_data = len(market_analysis)

            # length difference between all data and data received by client
            data_length_difference = length_of_all_data - length_of_data_received

            # if length difference is 0, it means client has received all available data
            if data_length_difference == 0: response = make_response('end of list'); response.status = 409; return response

            # if length difference is negative, it means client has set an invalid length of data received, received data cannot be greater than all available data
            if data_length_difference < 0: response = make_response('invalid length of data received'); response.status = 409; return response

            # only return signals client hasn't received yet **********************************************************
            # if timestamp_of_most_recent_signal_received and symbol_of_most_recent_signal_received are not '' or None or null(JS) or undefined (JS)
            if (
                (
                    timestamp_of_most_recent_signal_received != '' and
                    timestamp_of_most_recent_signal_received != None and
                    timestamp_of_most_recent_signal_received != 'undefined' and
                    timestamp_of_most_recent_signal_received != 'null'
                ) and 
                (
                    symbol_of_most_recent_signal_received != '' and
                    symbol_of_most_recent_signal_received != None and
                    symbol_of_most_recent_signal_received != 'undefined' and
                    symbol_of_most_recent_signal_received != 'null'
                )
            ):
                # find the index of the timestamp in market_analysis list, index of first occurance
                timestamp_index = next((i for i, signal in enumerate(market_analysis) if signal['timestamp'] == timestamp_of_most_recent_signal_received and signal['symbol'] == symbol_of_most_recent_signal_received), None)
                # *********************************************************************************
                # if index has been found *********************************************************
                if timestamp_index != None:
                    # make timestamp_index the end index and generate start_index *******
                    end_index = timestamp_index; start_index = end_index - client_load_more_increment
                    # *******************************************************************
                    # if the start_index happens to be negative, make it 0 **************
                    if start_index < 0: start_index = 0
                    # *******************************************************************
                # *********************************************************************************
                # if index has not been found, use default indexing for data fetch ****************
                else:
                    start_index = 0; end_index = start_index + client_load_more_increment
                # *********************************************************************************
            # ***********************************************************************************************
            # if timestamp_of_most_recent_signal_received is '' or None or or null (JS) or undefined (JS) ***
            else:
                # use default indexing for data fetch
                start_index = 0; end_index = start_index + client_load_more_increment
            # ***********************************************************************************************
            
            # perform data fetch by supplied indexes
            market_analysis = market_analysis[start_index:end_index]
            # *********************************************************************************************************
        # if client has not received any data yet
        else:
            # only return the first "client_load_more_increment" number of signals ************************************
            start_index = 0; end_index = start_index + client_load_more_increment
            market_analysis = market_analysis[start_index:end_index]
            # *********************************************************************************************************

    # return market analysis list (signals)
    response = make_response(jsonify(market_analysis)); response.status = 200; return response

# admin functions *****************************************************************************************************
# 13
@app.route('/getAllUsers', methods=['POST'])
def getAllUsers():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response
    
    # input field validation ********************
    # length of data received
    try: length_of_data_received = request.form['length_of_data_received'] 
    except: response = make_response('Length of data received field required'); response.status = 400; return response
    if length_of_data_received == '' or length_of_data_received == None: response = make_response('Length of data received cannot be empty'); response.status = 400; return response
    try: length_of_data_received = int(length_of_data_received)
    except: response = make_response('Length of data received data type is invalid'); response.status = 400; return response
    if length_of_data_received < 0: response = make_response('invalid length of data received'); response.status = 400; return response
    # get all
    try: get_all = request.form['get_all'] 
    except: response = make_response('Get all field required'); response.status = 400; return response
    if get_all == '' or get_all == None: response = make_response('Get all cannot be empty'); response.status = 400; return response
    try: get_all = ast.literal_eval(str(get_all).capitalize())
    except: response = make_response('Get all data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # get user list
    all_users = Users.objects.all()

    # modify user objects... delete passwords, add subscription status
    all_users = json.loads(all_users.to_json())
    all_users = [user_object_modification(i, current_datetime) for i in all_users]

    # if client did not request all data
    if get_all == False:
        # proceed to get client load more increment number
        client_load_more_increment = get_client_load_more_increment()

        # if client has already received some data
        if length_of_data_received > 0:
            # current length of all data
            length_of_all_data = len(all_users)

            # length difference between all data and data received by client
            data_length_difference = length_of_all_data - length_of_data_received

            # if length difference is 0, it means client has received all available data
            if data_length_difference == 0: response = make_response('end of list'); response.status = 409; return response

            # if length difference is negative, it means client has set an invalid length of data received, received data cannot be greater than all available data
            if data_length_difference < 0: response = make_response('invalid length of data received'); response.status = 409; return response

            # only return users client hasn't received yet
            start_index = length_of_data_received; end_index = start_index + client_load_more_increment
            all_users = all_users[start_index:end_index]

        # if client has not received any data yet
        else:
            # only return the first "client_load_more_increment" number of users
            start_index = 0; end_index = start_index + client_load_more_increment
            all_users = all_users[start_index:end_index]

    # return user list
    response = make_response(jsonify(all_users)); response.status = 200; return response

# 14
@app.route('/getUserCountryRanking', methods=['POST'])
def getUserCountryRanking():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get user list
    all_users = Users.objects.all()

    # create user country list
    processed_countries = []
    user_country_list = [
        {'country': i.country, 'users': len([z for z in all_users if z.country == i.country])} 
        for i in all_users if i.country not in processed_countries and not processed_countries.append(i.country)
    ]

    # return user country list
    response = make_response(jsonify(user_country_list)); response.status = 200; return response

# 15
@app.route('/getNewUserRegistrationStatistics', methods=['POST'])
def getNewUserRegistrationStatistics():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # start date
    try: start_date = request.form['start_date'] 
    except: response = make_response('Start date field required'); response.status = 400; return response
    # end date
    try: end_date = request.form['end_date'] 
    except: response = make_response('End date field required'); response.status = 400; return response
    # category
    try: category = request.form['category'] 
    except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    if isinstance(category, str) == False: response = make_response('Category data type is invalid'); response.status = 400; return response
    
    # get user list
    all_users = Users.objects.all()

    # return empty list if there are no users yet ... inorder to avoid errors by indexing empty list
    new_user_registration_statistics = []
    if len(all_users) == 0: response = make_response(jsonify(new_user_registration_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_users[0]['date_of_registration'][0:10] # start with first user's registration date in format yyyy-mm-dd
        end_date = str(datetime.now(timezone(system_timezone())))[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # date format validation
    try: datetime.strptime(start_date, date_format)
    except: response = make_response('invalid start date'); response.status = 400; return response
    try: datetime.strptime(end_date, date_format)
    except: response = make_response('invalid end date'); response.status = 400; return response

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days

    # if date difference is 0 days, change it to 1
    if date_difference_in_days == 0:
        date_difference_in_days = 1
    
    # list of days
    list_of_days = [str(datetime.strptime(start_date, date_format) + timedelta(days=i)) for i in range(date_difference_in_days)]

    # create new user registration statistics
    new_user_registration_statistics = [
        {'date': i[0:10], 'users': len([
            z for z in all_users if 
            i[0:10] == z.date_of_registration[0:10]
        ])}
        for i in list_of_days if True
    ]

    # return statistics
    response = make_response(jsonify(new_user_registration_statistics)); response.status = 200; return response

# 16
@app.route('/getNewSubscribedUserCountStatistics', methods=['POST'])
def getNewSubscribedUserCountStatistics():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # start date
    try: start_date = request.form['start_date'] 
    except: response = make_response('Start date field required'); response.status = 400; return response
    # end date
    try: end_date = request.form['end_date'] 
    except: response = make_response('End date field required'); response.status = 400; return response
    # category
    try: category = request.form['category'] 
    except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    if isinstance(category, str) == False: response = make_response('Category data type is invalid'); response.status = 400; return response
    
    # get subscriptions list
    all_subscriptions = Payments.objects.filter(purpose = 'subscription', verified=True)

    # return empty list if there are no subscriptions yet ... inorder to avoid errors by indexing empty list
    new_subscribed_user_statistics = []
    if len(all_subscriptions) == 0: response = make_response(jsonify(new_subscribed_user_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_subscriptions[0]['date'][0:10] # start with first subscription's date in format yyyy-mm-dd
        end_date = str(datetime.now(timezone(system_timezone())))[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # date format validation
    try: datetime.strptime(start_date, date_format)
    except: response = make_response('invalid start date'); response.status = 400; return response
    try: datetime.strptime(end_date, date_format)
    except: response = make_response('invalid end date'); response.status = 400; return response

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days

    # if date difference is 0 days, change it to 1
    if date_difference_in_days == 0:
        date_difference_in_days = 1
    
    # list of days
    list_of_days = [str(datetime.strptime(start_date, date_format) + timedelta(days=i)) for i in range(date_difference_in_days)]

    # create new subscribed user statistics
    new_subscribed_user_statistics = [
        {'date': i[0:10], 'users': len([
            z for z in all_subscriptions if 
            i[0:10] == z.date[0:10]
        ])}
        for i in list_of_days if True
    ]

    # return statistics
    response = make_response(jsonify(new_subscribed_user_statistics)); response.status = 200; return response

# 18
@app.route('/getUserPaymentHistoryByAccountId', methods=['POST'])
def getUserPaymentHistoryByAccountId():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    # length of data received
    try: length_of_data_received = request.form['length_of_data_received'] 
    except: response = make_response('Length of data received field required'); response.status = 400; return response
    if length_of_data_received == '' or length_of_data_received == None: response = make_response('Length of data received cannot be empty'); response.status = 400; return response
    try: length_of_data_received = int(length_of_data_received)
    except: response = make_response('Length of data received data type is invalid'); response.status = 400; return response
    if length_of_data_received < 0: response = make_response('invalid length of data received'); response.status = 400; return response
    # get all
    try: get_all = request.form['get_all'] 
    except: response = make_response('Get all field required'); response.status = 400; return response
    if get_all == '' or get_all == None: response = make_response('Get all cannot be empty'); response.status = 400; return response
    try: get_all = ast.literal_eval(str(get_all).capitalize())
    except: response = make_response('Get all data type is invalid'); response.status = 400; return response
    
    # collect payment history by user_id
    user_payment_history = Payments.objects.filter(user_id = account_id) # here we are not using verified=True because we want to be able to see unverified payments, and click a button to verify them, if the user gets in touch with us after paying but their payment wasn't updated when they tried verifying on their end
    user_payment_history = json.loads(user_payment_history.to_json())

    # if client did not request all data
    if get_all == False:
        # proceed to get client load more increment number
        client_load_more_increment = get_client_load_more_increment()

        # if client has already received some data
        if length_of_data_received > 0:
            # current length of all data
            length_of_all_data = len(user_payment_history)

            # length difference between all data and data received by client
            data_length_difference = length_of_all_data - length_of_data_received

            # if length difference is 0, it means client has received all available data
            if data_length_difference == 0: response = make_response('end of list'); response.status = 409; return response

            # if length difference is negative, it means client has set an invalid length of data received, received data cannot be greater than all available data
            if data_length_difference < 0: response = make_response('invalid length of data received'); response.status = 409; return response

            # only return payments client hasn't received yet
            start_index = length_of_data_received; end_index = start_index + client_load_more_increment
            user_payment_history = user_payment_history[start_index:end_index]

        # if client has not received any data yet
        else:
            # only return the first "client_load_more_increment" number of payments
            start_index = 0; end_index = start_index + client_load_more_increment
            user_payment_history = user_payment_history[start_index:end_index]

    # return payment history
    response = make_response(jsonify(user_payment_history)); response.status = 200; return response

# 19
@app.route('/searchForUser', methods=['POST'])
def searchForUser():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # search query
    try: search_query = request.form['search_query'] 
    except: response = make_response('Search query field required'); response.status = 400; return response
    if search_query == '' or search_query == None: response = make_response('Search query cannot be empty'); response.status = 400; return response
    if isinstance(search_query, str) == False: response = make_response('Search query data type is invalid'); response.status = 400; return response
    # length of data received
    try: length_of_data_received = request.form['length_of_data_received'] 
    except: response = make_response('Length of data received field required'); response.status = 400; return response
    if length_of_data_received == '' or length_of_data_received == None: response = make_response('Length of data received cannot be empty'); response.status = 400; return response
    try: length_of_data_received = int(length_of_data_received)
    except: response = make_response('Length of data received data type is invalid'); response.status = 400; return response
    if length_of_data_received < 0: response = make_response('invalid length of data received'); response.status = 400; return response
    # get all
    try: get_all = request.form['get_all'] 
    except: response = make_response('Get all field required'); response.status = 400; return response
    if get_all == '' or get_all == None: response = make_response('Get all cannot be empty'); response.status = 400; return response
    try: get_all = ast.literal_eval(str(get_all).capitalize())
    except: response = make_response('Get all data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # get user list
    all_users = Users.objects.all()

    # modify user objects... delete passwords, add subscription status
    all_users = json.loads(all_users.to_json())
    all_users = [user_object_modification(i, current_datetime) for i in all_users]

    # perform search
    user_results = [
        i for i in all_users if 
        search_query.lower() in i['email'].lower() or 
        search_query.lower() in i['username'].lower() or 
        search_query.lower() in i['firstname'].lower() or 
        search_query.lower() in i['lastname'].lower() or 
        search_query.lower() in i['phonenumber'].lower()
    ]

    # if client did not request all data
    if get_all == False:
        # proceed to get client load more increment number
        client_load_more_increment = get_client_load_more_increment()

        # if client has already received some data
        if length_of_data_received > 0:
            # current length of all data
            length_of_all_data = len(user_results)

            # length difference between all data and data received by client
            data_length_difference = length_of_all_data - length_of_data_received

            # if length difference is 0, it means client has received all available data
            if data_length_difference == 0: response = make_response('end of list'); response.status = 409; return response

            # if length difference is negative, it means client has set an invalid length of data received, received data cannot be greater than all available data
            if data_length_difference < 0: response = make_response('invalid length of data received'); response.status = 409; return response

            # only return users client hasn't received yet
            start_index = length_of_data_received; end_index = start_index + client_load_more_increment
            user_results = user_results[start_index:end_index]

        # if client has not received any data yet
        else:
            # only return the first "client_load_more_increment" number of users
            start_index = 0; end_index = start_index + client_load_more_increment
            user_results = user_results[start_index:end_index]

    # return user list
    response = make_response(jsonify(user_results)); response.status = 200; return response

# 20
@app.route('/getUserCountStatistics', methods=['POST'])
def getUserCountStatistics():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # start date
    try: start_date = request.form['start_date'] 
    except: response = make_response('Start date field required'); response.status = 400; return response
    # end date
    try: end_date = request.form['end_date'] 
    except: response = make_response('End date field required'); response.status = 400; return response
    # category
    try: category = request.form['category'] 
    except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    if isinstance(category, str) == False: response = make_response('Category data type is invalid'); response.status = 400; return response
    
    # get user list
    all_users = Users.objects.all()

    # return empty list if there are no users yet ... inorder to avoid errors by indexing empty list
    user_count_statistics = []
    if len(all_users) == 0: response = make_response(jsonify(user_count_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_users[0]['date_of_registration'][0:10] # start with first user's registration date in format yyyy-mm-dd
        end_date = str(datetime.now(timezone(system_timezone())))[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # date format validation
    try: datetime.strptime(start_date, date_format)
    except: response = make_response('invalid start date'); response.status = 400; return response
    try: datetime.strptime(end_date, date_format)
    except: response = make_response('invalid end date'); response.status = 400; return response

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days

    # if date difference is 0 days, change it to 1
    if date_difference_in_days == 0:
        date_difference_in_days = 1
    
    # list of days
    list_of_days = [str(datetime.strptime(start_date, date_format) + timedelta(days=i)) for i in range(date_difference_in_days)]

    # create user count statistics
    user_count_statistics = [
        {'date': i[0:10], 'users': len([
            z for z in all_users if 
            i[0:10] >= z.date_of_registration[0:10]
        ])}
        for i in list_of_days if True
    ]

    # return statistics
    response = make_response(jsonify(user_count_statistics)); response.status = 200; return response

# 21
@app.route('/getUserSubscriptionStatistics', methods=['POST'])
def getUserSubscriptionStatistics():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # start date
    try: start_date = request.form['start_date'] 
    except: response = make_response('Start date field required'); response.status = 400; return response
    # end date
    try: end_date = request.form['end_date'] 
    except: response = make_response('End date field required'); response.status = 400; return response
    # category
    try: category = request.form['category'] 
    except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    if isinstance(category, str) == False: response = make_response('Category data type is invalid'); response.status = 400; return response
    
    # get all payments
    all_payments = Payments.objects.filter(verified=True)

    # get subscriptions list
    all_subscriptions = [i for i in all_payments if 'subscription' in i.purpose.lower()]

    # return empty list if there are no subscriptions yet ... inorder to avoid errors by indexing empty list
    subscribed_user_statistics = []
    if len(all_subscriptions) == 0: response = make_response(jsonify(subscribed_user_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_subscriptions[0]['date'][0:10] # start with first subscription's date in format yyyy-mm-dd
        end_date = str(datetime.now(timezone(system_timezone())))[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # date format validation
    try: datetime.strptime(start_date, date_format)
    except: response = make_response('invalid start date'); response.status = 400; return response
    try: datetime.strptime(end_date, date_format)
    except: response = make_response('invalid end date'); response.status = 400; return response

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days

    # if date difference is 0 days, change it to 1
    if date_difference_in_days == 0:
        date_difference_in_days = 1
    
    # list of days
    list_of_days = [str(datetime.strptime(start_date, date_format) + timedelta(days=i)) for i in range(date_difference_in_days)]

    # create subscribed user statistics
    subscribed_user_statistics = [
        {'date': i[0:10], 'users': len([
            z for z in all_subscriptions if 
            i[0:10] >= z.date[0:10] and 
            i[0:10] < z.expiry_date[0:10]
        ])}
        for i in list_of_days if True
    ]

    # return statistics
    response = make_response(jsonify(subscribed_user_statistics)); response.status = 200; return response

# 22
@app.route('/getUserMetrics', methods=['POST'])
def getUserMetrics():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # get user list
    all_users = Users.objects.all()

    # modify user objects... delete passwords, add subscription status
    all_users = json.loads(all_users.to_json())
    all_users = [user_object_modification(i, current_datetime) for i in all_users]

    # get user metrics
    user_metrics = {
        'all_users': len(all_users),
        'subscribed_users': len([i for i in all_users if i['subscribed'] == True]),
        'users_not_subscribed': len([i for i in all_users if i['subscribed'] == False]),
        'banned_users': len([i for i in all_users if i['banned'] == True]),
        'verified_users': len([i for i in all_users if i['verified'] == True]),
        'users_not_verified': len([i for i in all_users if i['verified'] == False]),
        'verified_users_telegram': len([i for i in all_users if i['telegram_connected'] == True]),
        'users_not_verified_telegram': len([i for i in all_users if i['telegram_connected'] == False]),
        'admins': len([i for i in all_users if i['role'] == 'admin']),
        'free_users': len([i for i in all_users if i['role'] == 'free user'])
    }

    # return statistics
    response = make_response(jsonify(user_metrics)); response.status = 200; return response

# 23
@app.route('/banUser', methods=['POST'])
def banUser():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account id field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account id cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    # ban reason
    try: ban_reason = request.form['ban_reason'] 
    except: response = make_response('Ban reason field required'); response.status = 400; return response
    if ban_reason == '' or ban_reason == None: response = make_response('Ban reason cannot be empty'); response.status = 400; return response
    if isinstance(ban_reason, str) == False: response = make_response('Ban reason data type is invalid'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # check if admin password is correct
    admin = Users.objects.filter(id = user_id)[0]
    admin_encrypted_password = admin.password
    is_password_a_match = verify_encrypted_password(password, admin_encrypted_password)
    if is_password_a_match == False: 
        response = make_response('incorrect password'); response.status = 401; return response

    # proceed to get admin name and username
    admin_name_and_username = admin.firstname + ' ' + admin.lastname + ' (' + admin.username + ')'

    # check if user account exists and ban user
    try:
        # ban user
        Users.objects(id = account_id).update(
            banned = True,
            banned_by = admin_name_and_username,
            ban_reason = ban_reason,
            ban_time = current_datetime
        )

        # return response
        response = make_response('ok'); response.status = 200; return response
    except:
        response = make_response('invalid account id'); response.status = 404; return response

# 24
@app.route('/unbanUser', methods=['POST'])
def unbanUser():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # check if admin password is correct
    admin = Users.objects.filter(id = user_id)[0]
    admin_encrypted_password = admin.password
    is_password_a_match = verify_encrypted_password(password, admin_encrypted_password)
    if is_password_a_match == False: 
        response = make_response('incorrect password'); response.status = 401; return response

    # proceed to get admin name and username
    admin_name_and_username = admin.firstname + ' ' + admin.lastname + ' (' + admin.username + ')'

    # check if user account exists and unban user
    try:
        # unban user
        Users.objects(id = account_id).update(
            banned = False,
            unbanned_by = admin_name_and_username,
            unban_time = current_datetime
        )

        # return response
        response = make_response('ok'); response.status = 200; return response
    except:
        response = make_response('invalid account id'); response.status = 404; return response

# 25
@app.route('/changeUserRole', methods=['POST'])
def changeUserRole():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    # new role
    try: new_role = request.form['new_role'] 
    except: response = make_response('New role field required'); response.status = 400; return response
    if new_role == '' or new_role == None: response = make_response('New role cannot be empty'); response.status = 400; return response
    if isinstance(new_role, str) == False: response = make_response('New role data type is invalid'); response.status = 400; return response
    if new_role not in get_user_roles(): response = make_response('invalid role'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
        
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # check if admin password is correct
    admin = Users.objects.filter(id = user_id)[0]
    admin_encrypted_password = admin.password
    is_password_a_match = verify_encrypted_password(password, admin_encrypted_password)
    if is_password_a_match == False: 
        response = make_response('incorrect password'); response.status = 401; return response

    # proceed to get admin name and username
    admin_name_and_username = admin.firstname + ' ' + admin.lastname + ' (' + admin.username + ')'

    # user details
    user = Users.objects.filter(id = account_id)[0]

    # verifications *************************************************************************************************************
    # check if user has verified email ********************************************************************************
    if user.verified == False:
        response = make_response('email not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # check if user has verified telegram *****************************************************************************
    if user.telegram_connected == False:
        response = make_response('telegram not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # check if user account exists and change user role
    try:
        # old user role
        old_role = user.role

        # change user role
        Users.objects(id = account_id).update(
            role = new_role,
            role_issued_by  = admin_name_and_username
        )

        # notify user of role change **********************************************************************************
        # via email *****************************************************************************************
        send_account_role_change_email_notification(
            user.email, # email
            user.username,  # username
            user.firstname, # firstname
            user.lastname, # lastname
            old_role, # old role
            new_role # new role
        )
        # ***************************************************************************************************
        # via telegram **************************************************************************************
        if user.telegram_connected == True:
            send_account_role_change_telegram_notification(
                user.telegram_id, # telegram id
                user.username,  # username
                user.firstname, # firstname
                user.lastname, # lastname
                old_role, # old role
                new_role # new role
            )
        # ***************************************************************************************************
        # *************************************************************************************************************

        # return response
        response = make_response('ok'); response.status = 200; return response
    except:
        response = make_response('invalid account id'); response.status = 404; return response

# 26
@app.route('/manuallyEnterUserPayment', methods=['POST'])
def manuallyEnterUserPayment():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # account id
    try: account_id = request.form['account_id'] 
    except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    if isinstance(account_id, str) == False: response = make_response('Account ID data type is invalid'); response.status = 400; return response
    # purpose
    try: purpose = request.form['purpose']
    except: response = make_response('Purpose field required'); response.status = 400; return response
    if purpose == '' or purpose == None: response = make_response('Purpose cannot be empty'); response.status = 400; return response
    if purpose not in get_payment_purposes(): response = make_response('invalid purpose'); response.status = 400; return response
    if isinstance(purpose, str) == False: response = make_response('Purpose data type is invalid'); response.status = 400; return response
    # payment method
    try: payment_method = request.form['payment_method']
    except: response = make_response('Payment method field required'); response.status = 400; return response
    if payment_method == '' or payment_method == None: response = make_response('Payment method cannot be empty'); response.status = 400; return response
    if isinstance(payment_method, str) == False: response = make_response('Payment method data type is invalid'); response.status = 400; return response
    if payment_method not in get_payment_methods(): response = make_response('invalid method'); response.status = 400; return response
    # transaction id
    try: transaction_id = request.form['transaction_id']
    except: response = make_response('Transaction ID field required'); response.status = 400; return response
    if transaction_id == '' or transaction_id == None: response = make_response('Transaction ID cannot be empty'); response.status = 400; return response
    if isinstance(transaction_id, str) == False: response = make_response('Transaction ID data type is invalid'); response.status = 400; return response
    # discount applied
    try: discount_applied = request.form['discount_applied']
    except: response = make_response('Discount applied field required'); response.status = 400; return response
    if discount_applied == '' or discount_applied == None: response = make_response('Discount applied cannot be empty'); response.status = 400; return response
    try: discount_applied = float(discount_applied)
    except: response = make_response('Discount data type is invalid'); response.status = 400; return response
    if discount_applied < 0: response = make_response('Discount applied cannot be less than 0'); response.status = 400; return response
    # amount
    try: amount = request.form['amount']
    except: response = make_response('Amount field required'); response.status = 400; return response
    if amount == '' or amount == None: response = make_response('Amount cannot be empty'); response.status = 400; return response
    try: amount = float(amount)
    except: response = make_response('Amount data type is invalid'); response.status = 400; return response
    if amount < 0: response = make_response('Amount cannot be less than 0'); response.status = 400; return response
    # password
    try: password = request.form['password'] 
    except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if isinstance(password, str) == False: response = make_response('Password data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'

    # check if admin password is correct
    admin = Users.objects.filter(id = user_id)[0]
    admin_encrypted_password = admin.password
    is_password_a_match = verify_encrypted_password(password, admin_encrypted_password)
    if is_password_a_match == False: 
        response = make_response('incorrect password'); response.status = 401; return response

    # proceed to get admin name and username
    admin_name_and_username = admin.firstname + ' ' + admin.lastname + ' (' + admin.username + ')'

    # check if user account exists
    user = None
    try:
        # check if user account exists
        user = Users.objects.filter(id = account_id)[0]
    except:
        response = make_response('invalid account id'); response.status = 404; return response

    # verifications *************************************************************************************************************
    # check if user has verified email ********************************************************************************
    if user.verified == False:
        response = make_response('email not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # check if user has verified telegram *****************************************************************************
    if user.telegram_connected == False:
        response = make_response('telegram not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # if purpose is a Monthly Subscription / Yearly Subscription
    expiry_date = ''
    if 'subscription' in purpose.lower():
        # check if amount is sufficient
        if amount < 10 or amount % 10 != 0 and amount != 96:
            response = make_response('enter sufficient amount for a subscription'); response.status = 404; return response
        
        # check if amount does not exceed max subscription package
        if amount > 96:
            response = make_response('subscription amount cannot be more than max subscription'); response.status = 404; return response

        # determine subscription expiry *****************************************************************************************
        # get subscription months by amount
        if amount == 96: subscription_months = 12
        else: subscription_months = amount / 10

        # get subscription weeks
        subscription_weeks = subscription_months * 4

        # get user subscription status and subscription expiry date (free trial counts)
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)

        # if user has an active subscription or free trial
        if user_subscribed == True: expiry_date = str(datetime.strptime(subcription_expiry_date, date_format) + timedelta(weeks = subscription_weeks))
        # if user has no active subscription
        else: expiry_date = str(current_datetime_object + timedelta(weeks = subscription_weeks))
        # ***********************************************************************************************************************
        
        # set new subscription and subscription expiry dates to the user's account **********************************************
        Users.objects(id = account_id).update(
            subscription_date = current_datetime,
            subscription_expiry = expiry_date,
            subscription_expiring_soon_notification_issued = False,
            subscription_expired_notification_issued = False
        )
        # ***********************************************************************************************************************

    # add user payment
    payment_details = Payments(
        date = current_datetime,
        user_id = account_id,
        purpose = purpose,
        payment_method = payment_method,
        transaction_id = transaction_id,
        verified = True,
        discount_applied = discount_applied,
        amount = float(amount),
        expiry_date = expiry_date,
        entered_by = admin_name_and_username
    )
    payment_details.save()

    # return response
    response = make_response('ok'); response.status = 200; return response

# 27
@app.route('/getEarningsReport', methods=['POST'])
def getEarningsReport():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # start date
    try: start_date = request.form['start_date'] 
    except: response = make_response('Start date field required'); response.status = 400; return response
    # end date
    try: end_date = request.form['end_date'] 
    except: response = make_response('End date field required'); response.status = 400; return response

    # get all payments
    all_payments = Payments.objects.filter(verified = True)

    # initialize earnings report variable
    earnings_report = {}

    # if no dates have been given
    if (start_date == '' or start_date == None) and (end_date == '' or end_date == None):
        # total earnings
        total_earnings = sum([i.amount for i in all_payments if True])
        earnings_report['total_earnings'] = total_earnings

        # subscriptions
        subscriptions = sum([i.amount for i in all_payments if 'subscription' in i.purpose.lower()])
        earnings_report['subscriptions'] = subscriptions

        # payment methods
        payment_methods = get_payment_methods()
        for payment_method in payment_methods:
            earnings_report[payment_method] = sum([i.amount for i in all_payments if i.payment_method == payment_method])

    # if only start date has been given
    if (start_date != '' and start_date != None) and (end_date == '' or end_date == None):
        # date format validation
        try: datetime.strptime(start_date, '%Y-%m-%d')
        except: response = make_response('invalid start date'); response.status = 400; return response
        
        # total earnings
        total_earnings = sum([i.amount for i in all_payments if i.date[0:10] >= start_date])
        earnings_report['total_earnings'] = total_earnings

        # subscriptions
        subscriptions = sum([i.amount for i in all_payments if 'subscription' in i.purpose.lower() and i.date[0:10] >= start_date])
        earnings_report['subscriptions'] = subscriptions

        # payment methods
        payment_methods = get_payment_methods()
        for payment_method in payment_methods:
            method_earnings = sum([i.amount for i in all_payments if i.payment_method == payment_method and i.date[0:10] >= start_date])
            earnings_report[payment_method] = method_earnings

    # if only end date has been given
    if (start_date == '' or start_date == None) and (end_date != '' and end_date != None):
        # date format validation
        try: datetime.strptime(end_date, '%Y-%m-%d')
        except: response = make_response('invalid end date'); response.status = 400; return response

        # total earnings
        total_earnings = sum([i.amount for i in all_payments if i.date[0:10] <= end_date])
        earnings_report['total_earnings'] = total_earnings

        # subscriptions
        subscriptions = sum([i.amount for i in all_payments if 'subscription' in i.purpose.lower() and i.date[0:10] <= end_date])
        earnings_report['subscriptions'] = subscriptions

        # payment methods
        payment_methods = get_payment_methods()
        for payment_method in payment_methods:
            method_earnings = sum([i.amount for i in all_payments if i.payment_method == payment_method and i.date[0:10] <= end_date])
            earnings_report[payment_method] = method_earnings

    # if both dates have been given
    if (start_date != '' and start_date != None) and (end_date != '' and end_date != None):
        # date format validation
        try: datetime.strptime(start_date, '%Y-%m-%d')
        except: response = make_response('invalid start date'); response.status = 400; return response
        try: datetime.strptime(end_date, '%Y-%m-%d')
        except: response = make_response('invalid end date'); response.status = 400; return response
        
        # total earnings
        total_earnings = sum([i.amount for i in all_payments if i.date[0:10] >= start_date and i.date[0:10] <= end_date])
        earnings_report['total_earnings'] = total_earnings

        # subscriptions
        subscriptions = sum([i.amount for i in all_payments if 'subscription' in i.purpose.lower()and i.date[0:10] >= start_date and i.date[0:10] <= end_date])
        earnings_report['subscriptions'] = subscriptions

        # payment methods
        payment_methods = get_payment_methods()
        for payment_method in payment_methods:
            method_earnings = sum([i.amount for i in all_payments if i.payment_method == payment_method and i.date[0:10] >= start_date and i.date[0:10] <= end_date])
            earnings_report[payment_method] = method_earnings

    # return response
    response = make_response(jsonify(earnings_report)); response.status = 200; return response

# 28
@app.route('/getPaymentsList', methods=['POST'])
def getPaymentsList():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # start date
    try: start_date = request.form['start_date'] 
    except: response = make_response('Start date field required'); response.status = 400; return response
    # end date
    try: end_date = request.form['end_date'] 
    except: response = make_response('End date field required'); response.status = 400; return response
    # entered by
    try: entered_by = request.form['entered_by'] 
    except: response = make_response('Entered by field required'); response.status = 400; return response
    if entered_by != '' and entered_by != None and isinstance(entered_by, str) == False: response = make_response('Entered by data type is invalid'); response.status = 400; return response
    # length of data received
    try: length_of_data_received = request.form['length_of_data_received'] 
    except: response = make_response('Length of data received field required'); response.status = 400; return response
    if length_of_data_received == '' or length_of_data_received == None: response = make_response('Length of data received cannot be empty'); response.status = 400; return response
    try: length_of_data_received = int(length_of_data_received)
    except: response = make_response('Length of data received data type is invalid'); response.status = 400; return response
    if length_of_data_received < 0: response = make_response('invalid length of data received'); response.status = 400; return response
    # get all
    try: get_all = request.form['get_all'] 
    except: response = make_response('Get all field required'); response.status = 400; return response
    if get_all == '' or get_all == None: response = make_response('Get all cannot be empty'); response.status = 400; return response
    try: get_all = ast.literal_eval(str(get_all).capitalize())
    except: response = make_response('Get all data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)

    # get all payments
    all_payments = Payments.objects.filter(verified = True)
    all_payments = json.loads(all_payments.to_json())

    # if entered by has been given
    if entered_by != '' and entered_by != None:
        all_payments = [i for i in all_payments if entered_by.lower() in i['entered_by'].lower()]

    # if no dates have been given
    if (start_date == '' or start_date == None) and (end_date == '' or end_date == None):
        all_payments = [i for i in all_payments if True]

    # if only start date has been given
    if (start_date != '' and start_date != None) and (end_date == '' or end_date == None):
        # date format validation
        try: datetime.strptime(start_date, '%Y-%m-%d')
        except: response = make_response('invalid start date'); response.status = 400; return response
        
        # proceed to get data
        all_payments = [i for i in all_payments if i['date'][0:10] >= start_date]

    # if only end date has been given
    if (start_date == '' or start_date == None) and (end_date != '' and end_date != None):
        # date format validation
        try: datetime.strptime(end_date, '%Y-%m-%d')
        except: response = make_response('invalid end date'); response.status = 400; return response
        
        # proceed to get data
        all_payments = [i for i in all_payments if i['date'][0:10] <= end_date]

    # if both dates have been given
    if (start_date != '' and start_date != None) and (end_date != '' and end_date != None):
        # date format validation
        try: datetime.strptime(start_date, '%Y-%m-%d')
        except: response = make_response('invalid start date'); response.status = 400; return response
        try: datetime.strptime(end_date, '%Y-%m-%d')
        except: response = make_response('invalid end date'); response.status = 400; return response
        
        # proceed to get data
        all_payments = [i for i in all_payments if i['date'][0:10] >= start_date and i['date'][0:10] <= end_date]

    # if client did not request all data
    if get_all == False:
        # proceed to get client load more increment number
        client_load_more_increment = get_client_load_more_increment()

        # if client has already received some data
        if length_of_data_received > 0:
            # current length of all data
            length_of_all_data = len(all_payments)

            # length difference between all data and data received by client
            data_length_difference = length_of_all_data - length_of_data_received

            # if length difference is 0, it means client has received all available data
            if data_length_difference == 0: response = make_response('end of list'); response.status = 409; return response

            # if length difference is negative, it means client has set an invalid length of data received, received data cannot be greater than all available data
            if data_length_difference < 0: response = make_response('invalid length of data received'); response.status = 409; return response

            # only return payments client hasn't received yet
            start_index = length_of_data_received; end_index = start_index + client_load_more_increment
            all_payments = all_payments[start_index:end_index]

        # if client has not received any data yet
        else:
            # only return the first "client_load_more_increment" number of payments
            start_index = 0; end_index = start_index + client_load_more_increment
            all_payments = all_payments[start_index:end_index]

    # return response
    response = make_response(jsonify(all_payments)); response.status = 200; return response

# payment functions ***********************************************************************************************************************
# Paynow ************************************************************************************************************************
# 31
@app.route('/initiatePaynowPayment', methods=['POST'])
def initiatePaynowPayment():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # method ... ecocash / onemoney
    try: method = request.form['method'] 
    except: response = make_response('Method field required'); response.status = 400; return response
    if method == '' or method == None: response = make_response('Method cannot be empty'); response.status = 400; return response
    if isinstance(method, str) == False: response = make_response('Method data type is invalid'); response.status = 400; return response
    # phonenumber ... 07XX XXX XXX
    try: phonenumber = request.form['phonenumber'] 
    except: response = make_response('Phonenumber field required'); response.status = 400; return response
    if phonenumber == '' or phonenumber == None: response = make_response('Phonenumber cannot be empty'); response.status = 400; return response
    if isinstance(phonenumber, str) == False: response = make_response('Phonenumber data type is invalid'); response.status = 400; return response
    # currency ... USD / ZWG
    try: currency = request.form['currency'] 
    except: response = make_response('Currency field required'); response.status = 400; return response
    if currency == '' or currency == None: response = make_response('Currency cannot be empty'); response.status = 400; return response
    if isinstance(currency, str) == False: response = make_response('Currency data type is invalid'); response.status = 400; return response
    # subscription type ... Monthly Subscription, Yearly Subscription
    try: subscription_type = request.form['subscription_type'] 
    except: response = make_response('Subscription type field required'); response.status = 400; return response
    if subscription_type == '' or subscription_type == None: response = make_response('Subscription type cannot be empty'); response.status = 400; return response
    if isinstance(subscription_type, str) == False: response = make_response('Subscription type data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'

    # user details
    user = Users.objects.filter(id = user_id)[0]

    # verifications *************************************************************************************************************
    # check if user has verified email ********************************************************************************
    if user.verified == False:
        response = make_response('email not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # check if user has verified telegram *****************************************************************************
    if user.telegram_connected == False:
        response = make_response('telegram not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # determine amount by subscription_type
    if subscription_type == 'Monthly Subscription': amount = 10.00; discount_applied = 0
    elif subscription_type == 'Yearly Subscription': amount = 96.00; discount_applied = 0
    else: response = make_response('unknown subscription type'); response.status = 404; return response

    # initiate Paynow transaction
    transaction_initiation_successful, poll_url = paynow_payment(
        subscription_type, # purpose
        subscription_type, # item
        user.email, # user email ... use account email for sandbox tests
        method.lower(), # payment method ... ecocash / onemoney
        phonenumber.replace(' ', ''), # payment phonenumber
        amount, # amount
        currency # currency ... USD / ZWG
    )

    # structure payment method in a way that matches its representation in get_payment_methods() within settings.py
    method = method + ' ' + currency

    # if transaction failed to initiate
    if transaction_initiation_successful == False: response = make_response('failed to initiate'); response.status = 404; return response

    # if transaction was initiated successfully, add it as an unverified payment to Payments
    if transaction_initiation_successful == True:
        # determine subscription expiry *****************************************************************************************
        # get subscription months by amount
        if amount == 96: subscription_months = 12
        else: subscription_months = amount / 10

        # get subscription weeks
        subscription_weeks = subscription_months * 4

        # get user subscription status and subscription expiry date (free trial counts)
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)

        # if user has an active subscription or free trial
        if user_subscribed == True: expiry_date = str(datetime.strptime(subcription_expiry_date, date_format) + timedelta(weeks = subscription_weeks))
        # if user has no active subscription
        else: expiry_date = str(current_datetime_object + timedelta(weeks = subscription_weeks))
        # ***********************************************************************************************************************

        # add user payment
        payment_details = Payments(
            date = current_datetime,
            user_id = user_id,
            purpose = subscription_type,
            payment_method = method,
            transaction_id = poll_url,
            verified = False, # will be verified if status is found as paid in checkPaynowTransactionStatus
            discount_applied = discount_applied,
            amount = float(amount),
            expiry_date = expiry_date,
            entered_by = 'system (Paynow Gateway)'
        )
        payment_details.save()

        # return response
        response = make_response('initiation successful'); response.status = 200; return response

# 32
@app.route('/checkPaynowTransactionStatus', methods=['POST'])
def checkPaynowTransactionStatus():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # if request was made by an admin account ***********************************************************************************
    if user_role == 'admin':
        # input field validation ********************
        # account id
        try: account_id = request.form['account_id'] 
        except: response = make_response('Account ID field required'); response.status = 400; return response
        # if request is not for the admin's own account
        if account_id != 'self' and account_id != '' and account_id != None and account_id != 'null': 
            user_id = account_id
            # validation of supplied account id
            try: account = Users.objects.filter(id = account_id)[0]
            except: response = make_response('invalid account id'); response.status = 404; return response
    # ***************************************************************************************************************************
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'

    # user details
    user = Users.objects.filter(id = user_id)[0]

    # if user's most recent transaction has been verified already ***************************************************************
    # get all user payments
    user_payments = Payments.objects.filter(user_id = user_id, entered_by = 'system (Paynow Gateway)')
    # get user's most recent payment's verification status
    if len(user_payments) > 0: most_recent_payment_verified = user_payments[len(user_payments)-1].verified
    else: most_recent_payment_verified = False
    # ***************************************************************************************************************************

    # user's pending payments
    user_pending_payments = Payments.objects.filter(user_id = user_id, entered_by = 'system (Paynow Gateway)', verified = False)

    # if user has no pending payments or user's most recent payment's verification status = True
    if len(user_pending_payments) == 0 or most_recent_payment_verified == True: response = make_response('no pending payments'); response.status = 404; return response

    # user's most recent pending payment
    most_recent_pending_payment = user_pending_payments[len(user_pending_payments)-1]

    # get user's most recent poll url
    most_recent_poll_url = most_recent_pending_payment.transaction_id

    # get user's most recent payment amount
    amount = most_recent_pending_payment.amount

    # get user's most recent payment method
    method = most_recent_pending_payment.method

    # get user's most recent payment currency
    currency = 'USD' if 'USD' in method else 'ZWG'

    # check Paynow transaction status ... sent / paid / cancelled
    payment_status = paynow_status(most_recent_poll_url, currency)

    # if transaction has not been paid
    if payment_status != 'paid': response = make_response('not paid'); response.status = 404; return response

    # if transaction has been paid
    if payment_status == 'paid':
        # determine subscription expiry *****************************************************************************************
        # get subscription months by amount
        if amount == 96: subscription_months = 12
        else: subscription_months = amount / 10

        # get subscription weeks
        subscription_weeks = subscription_months * 4

        # get user subscription status and subscription expiry date (free trial counts)
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)

        # if user has an active subscription or free trial
        if user_subscribed == True: expiry_date = str(datetime.strptime(subcription_expiry_date, date_format) + timedelta(weeks = subscription_weeks))
        # if user has no active subscription
        else: expiry_date = str(current_datetime_object + timedelta(weeks = subscription_weeks))
        # ***********************************************************************************************************************

        # set new subscription and subscription expiry dates to the user's account **********************************************
        Users.objects(id = user_id).update(
            subscription_date = current_datetime,
            subscription_expiry = expiry_date,
            subscription_expiring_soon_notification_issued = False,
            subscription_expired_notification_issued = False
        )
        # ***********************************************************************************************************************

        # mark payment as verified **********************************************************************************************
        Payments.object(id = str(most_recent_pending_payment.id)).update(
            verified = True
        )
        # ***********************************************************************************************************************

        # send payment confirmation messages to user ****************************************************************************
        # email *******************************************************************************************************
        send_payment_confirmation_email(
            user.email, # email
            user.username, # username
            user.firstname, # firstname
            user.lastname, # lastname
            most_recent_pending_payment.amount, # amount
            True, # subscription -> true or false
            most_recent_pending_payment.purpose # subscription package
        )
        # *************************************************************************************************************
        # telegram ****************************************************************************************************
        if user.telegram_connected == True:
            send_payment_confirmation_telegram_notification(
                user.telegram_id, # telegram id
                user.username, # username
                user.firstname, # firstname
                user.lastname, # lastname
                most_recent_pending_payment.amount, # amount
                True, # subscription -> true or false
                most_recent_pending_payment.purpose # subscription package
            )
        # *************************************************************************************************************
        # ***********************************************************************************************************************

        # return response 
        response = make_response('paid'); response.status = 200; return response
# *******************************************************************************************************************************
# Oxapay ************************************************************************************************************************
# 33
@app.route('/initiateOxapayPayment', methods=['POST'])
def initiateOxapayPayment():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation ********************
    # subscription type ... Monthly Subscription, Yearly Subscription
    try: subscription_type = request.form['subscription_type'] 
    except: response = make_response('Subscription type field required'); response.status = 400; return response
    if subscription_type == '' or subscription_type == None: response = make_response('Subscription type cannot be empty'); response.status = 400; return response
    if isinstance(subscription_type, str) == False: response = make_response('Subscription type data type is invalid'); response.status = 400; return response
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'

    # user details
    user = Users.objects.filter(id = user_id)[0]

    # verifications *************************************************************************************************************
    # check if user has verified email ********************************************************************************
    if user.verified == False:
        response = make_response('email not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # check if user has verified telegram *****************************************************************************
    if user.telegram_connected == False:
        response = make_response('telegram not verified'); response.status = 403; return response
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # determine amount by subscription_type
    if subscription_type == 'Monthly Subscription': amount = 10.00; discount_applied = 0
    elif subscription_type == 'Yearly Subscription': amount = 96.00; discount_applied = 0
    else: response = make_response('unknown subscription type'); response.status = 404; return response

    # initiate Oxapay transaction
    transaction_initiation_successful, track_id, paylink = oxapay_payment(
        amount, # amount
        subscription_type, # description
        user.email + '-' + current_datetime, # order id
        user.email # user email
    )

    # if transaction failed to initiate
    if transaction_initiation_successful == False: response = make_response('failed to initiate'); response.status = 404; return response

    # if transaction was initiated successfully, add it as an unverified payment to Payments
    if transaction_initiation_successful == True:
        # determine subscription expiry *****************************************************************************************
        # get subscription months by amount
        if amount == 96: subscription_months = 12
        else: subscription_months = amount / 10

        # get subscription weeks
        subscription_weeks = subscription_months * 4

        # get user subscription status and subscription expiry date (free trial counts)
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)

        # if user has an active subscription or free trial
        if user_subscribed == True: expiry_date = str(datetime.strptime(subcription_expiry_date, date_format) + timedelta(weeks = subscription_weeks))
        # if user has no active subscription
        else: expiry_date = str(current_datetime_object + timedelta(weeks = subscription_weeks))
        # ***********************************************************************************************************************

        # add user payment
        payment_details = Payments(
            date = current_datetime,
            user_id = user_id,
            purpose = subscription_type,
            payment_method = 'To be confirmed after user has paid (via Oxapay)',
            transaction_id = track_id,
            verified = False, # will be verified if status is found as paid in checkOxapayTransactionStatus
            discount_applied = discount_applied,
            amount = float(amount),
            expiry_date = expiry_date,
            entered_by = 'system (Oxapay Gateway)'
        )
        payment_details.save()

        # return response
        response = make_response(paylink); response.status = 200; return response

# 34
@app.route('/checkOxapayTransactionStatus', methods=['POST'])
def checkOxapayTransactionStatus():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin/free user') # request data, expected user roles separated by "/" if more than one
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # if request was made by an admin account ***********************************************************************************
    if user_role == 'admin':
        # input field validation ********************
        # account id
        try: account_id = request.form['account_id'] 
        except: response = make_response('Account ID field required'); response.status = 400; return response
        # if request is not for the admin's own account
        if account_id != 'self' and account_id != '' and account_id != None and account_id != 'null': 
            user_id = account_id
            # validation of supplied account id
            try: account = Users.objects.filter(id = account_id)[0]
            except: response = make_response('invalid account id'); response.status = 404; return response
    # ***************************************************************************************************************************
    
    # get current datetime
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'

    # user details
    user = Users.objects.filter(id = user_id)[0]

    # if user's most recent transaction has been verified already ***************************************************************
    # get all user payments
    user_payments = Payments.objects.filter(user_id = user_id, entered_by = 'system (Oxapay Gateway)')
    # get user's most recent payment's verification status
    if len(user_payments) > 0: most_recent_payment_verified = user_payments[len(user_payments)-1].verified
    else: most_recent_payment_verified = False
    # ***************************************************************************************************************************

    # user's pending payments
    user_pending_payments = Payments.objects.filter(user_id = user_id, entered_by = 'system (Oxapay Gateway)', verified = False)

    # if user has no pending payments or user's most recent payment's verification status = True
    if len(user_pending_payments) == 0 or most_recent_payment_verified == True: response = make_response('no pending payments'); response.status = 404; return response

    # user's most recent pending payment
    most_recent_pending_payment = user_pending_payments[len(user_pending_payments)-1]

    # get user's most recent track id
    most_recent_track_id = most_recent_pending_payment.transaction_id

    # get user's most recent payment amount
    amount = most_recent_pending_payment.amount

    # check oxapay transaction status ... status of the payment (e.g., \"New,\" \"Waiting,\" \"Confirming,\" \"Paid,\" \"Expired,\" etc.)
    transaction_status_check_successful, status, network = oxapay_status(most_recent_track_id)

    # if transaction has not been paid
    if status != 'Paid' or transaction_status_check_successful != True: response = make_response('not paid'); response.status = 404; return response

    # if transaction has been paid
    if status == 'Paid' and transaction_status_check_successful == True:
        # determine subscription expiry *****************************************************************************************
        # get subscription months by amount
        if amount == 96: subscription_months = 12
        else: subscription_months = amount / 10

        # get subscription weeks
        subscription_weeks = subscription_months * 4

        # get user subscription status and subscription expiry date (free trial counts)
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)

        # if user has an active subscription or free trial
        if user_subscribed == True: expiry_date = str(datetime.strptime(subcription_expiry_date, date_format) + timedelta(weeks = subscription_weeks))
        # if user has no active subscription
        else: expiry_date = str(current_datetime_object + timedelta(weeks = subscription_weeks))
        # ***********************************************************************************************************************

        # set new subscription and subscription expiry dates to the user's account **********************************************
        Users.objects(id = user_id).update(
            subscription_date = current_datetime,
            subscription_expiry = expiry_date,
            subscription_expiring_soon_notification_issued = False,
            subscription_expired_notification_issued = False
        )
        # ***********************************************************************************************************************

        # mark payment as verified **********************************************************************************************
        Payments.object(id = str(most_recent_pending_payment.id)).update(
            verified = True
        )
        # ***********************************************************************************************************************

        # send payment confirmation messages to user ****************************************************************************
        # email *******************************************************************************************************
        send_payment_confirmation_email(
            user.email, # email
            user.username, # username
            user.firstname, # firstname
            user.lastname, # lastname
            most_recent_pending_payment.amount, # amount
            True, # subscription -> true or false
            most_recent_pending_payment.purpose # subscription package
        )
        # *************************************************************************************************************
        # telegram ****************************************************************************************************
        if user.telegram_connected == True:
            send_payment_confirmation_telegram_notification(
                user.telegram_id, # telegram id
                user.username, # username
                user.firstname, # firstname
                user.lastname, # lastname
                most_recent_pending_payment.amount, # amount
                True, # subscription -> true or false
                most_recent_pending_payment.purpose # subscription package
            )
        # *************************************************************************************************************
        # ***********************************************************************************************************************

        # return response 
        response = make_response('paid'); response.status = 200; return response
# *******************************************************************************************************************************
# *****************************************************************************************************************************************

if __name__ == '__main__':
    init_db()
    # app.run(host='0.0.0.0') # for development
    # app.run(host=os.environ.get("BACKEND_HOST", "0.0.0.0"), port=5000) # for development use in docker
    # from waitress import serve
    # serve(app, host='0.0.0.0') # use waitress... for production