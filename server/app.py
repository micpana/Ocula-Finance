# imports
from flask import Flask, request, send_file, jsonify, make_response
from flask_cors import CORS, cross_origin
from user_agents import parse
import json
import re
from datetime import datetime, timedelta
from database import init_db
from models import  Users, EmailVerifications, UserAccessTokens, PasswordRecoveries, MarketAnalysisPayments, LoginTrials, Payments
from encryption import encrypt_password, verify_encrypted_password
from emails import send_registration_email_confirmation, send_password_recovery_email, send_email_change_confirmation, send_login_on_new_device_email_notification, send_account_email_change_email_notification
from settings import frontend_client_url, verification_token_expiration_minutes, access_token_expiration_days, token_send_on_user_request_retry_period_in_minutes

# Flask stuff
app = Flask(__name__)
app.debug = True

# Cross Origin Stuff
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
# app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
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
    trial_details = LoginTrials(
        account_id = account_id,
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
    
    # if login trial was a success + device is a new login device by user, notify user via email
    if status == True:
        # check if user has used the device before
        matches = LoginTrials.objects.filter(account_id = account_id, device = device, os = user_os, browser = browser)
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
                user_browser
            ) # inputs: user_email, username, firstname, lastname, date_and_time, user_os, user_device, user_ip_address, user_browser

    return 'ok'

# function for checking a user access token's validity
def check_user_access_token_validity(request_data, expected_user_role):
    try:
        # get user access token
        user_access_token = request_data.headers.get('access_token')
        # get information on user's browsing device
        user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request_data)
        # check token's validity while trying to retrieve the user's system id
        token_details = UserAccessTokens.objects.filter(
            id = user_access_token, 
            active = True, 
            user_browsing_agent = user_browsing_agent
        )[0]
        # get user id
        user_id = token_details.user_id
        # get user role
        user_role = Users.objects.filter(id = user_id)[0].role
        # get current date and time
        current_datetime = str(datetime.now())
        # get access token status
        if token_details.active == False:
            access_token_status = 'Access token disabled via signout'
        elif current_datetime > token_details.expiry_date:
            access_token_status = 'Access token expired'
        
        
            # check if user account's role matches expected user role
            if user_role not in expected_user_role.split('/'): return 'Not authorized to access this'
            # proceed since everything checks out
            access_token_status = 'ok'
            # show that access token was last used now
            AccessTokens.objects(id = user_access_token).update(last_used_on_date = current_datetime)
        # return access_token_status, user_id, user_role
        return access_token_status, user_id, user_role
    except:
        return 'Invalid token', None

# email structure validation
def is_email_structure_valid(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
        return True
    
    
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
    # input field validation
    try: firstname = request.form['firstname'] except: response = make_response('Firstname field required'); response.status = 400; return response
    if firstname == '' or firstname == None: response = make_response('Firstname cannot be empty'); response.status = 400; return response
    try: lastname = request.form['lastname'] except: response = make_response('Lastname field required'); response.status = 400; return response
    if lastname == '' or lastname == None: response = make_response('Lastname cannot be empty'); response.status = 400; return response
    try: username = request.form['username'] except: response = make_response('Username field required'); response.status = 400; return response
    if username == '' or username == None: response = make_response('Username cannot be empty'); response.status = 400; return response
    try: email = request.form['email'] except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('Invalid email structure') ; response.status = 400; return response
    try: phonenumber = request.form['phonenumber'] except: response = make_response('Phonenumber field required'); response.status = 400; return response
    if phonenumber == '' or phonenumber == None: response = make_response('Phonenumber cannot be empty'); response.status = 400; return response
    try: password = request.form['password'] except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if is_password_structure_valid(password) == False: response = make_response('Invalid password structure'); response.status = 400; return response
    try: country = request.form['country'] except: response = make_response('Country field required'); response.status = 400; return response
    if country == '' or country == None: response = make_response('Country cannot be empty'); response.status = 400; return response

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
        date_of_registration = str(datetime.now())
        verified = False,
        subscription_date = '',
        subscription_expiry = '',
        role = 'user',
        banned = False
    )
    account_details = user_details.save()
    account_id = account_details.id

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
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
        date_of_request = current_datetime
        expiry_date = token_expiration_date
    )
    verification_details = email_verification_details.save()
    email_verification_token = verification_details.id

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
    return response = make_response(account_id); response.status = 201; return response

# 2
@app.route('/signin', methods=['POST'])
def signin():
    # input field validation
    try: email_or_username = request.form['email_or_username'] except: response = make_response('Email or username field required'); response.status = 400; return response
    if email_or_username == '' or email_or_username == None: response = make_response('Email or username cannot be empty'); response.status = 400; return response
    try: password = request.form['password'] except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
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
            account_id = match.id,
            email = match.email,
            purpose = 'registration email', # registration email / email change 
            used = False,
            device = user_device,
            ip_address = user_ip_address,
            date_of_request = current_datetime
            expiry_date = token_expiration_date
        )
        verification_details = email_verification_details.save()
        email_verification_token = verification_details.id

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
        user_id = match.id,
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
    saved_token_details = token_details.save()
    token_id =saved_token_details.id
    user_access_token = generated_access_token + '.' + token_id
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
    response = make_response(user_access_token); response.status = 200; return response

# 17
@app.route('/getUserVerificationEmailByUserId', methods=['POST'])
def getUserVerificationEmailByUserId():
    # field validation
    try: account_id = request.form['account_id'] except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response

    # search for user by given userid
    matches = Users.objects.filter(id = account_id)
    if len(matches) == 0: response = make_response('invalid'); response.status = 404; return response

    # user data
    user = matches[0]

    # check if user verification status
    if user.verified == True: response = make_response('already verified'); response.status = 409; return response

    # check if last verification token by user hasn't expired
    last_user_token = EmailVerifications.objects.filter(account_id = account_id)[-1]
    if str(datetime.now()) > last_user_token.expiry_date: response = make_response('redirect to signin'); response.status = 401; return response
    
    # get user email
    user_email = user.email
    
    # return user email
    response = make_response(user_email); response.status = 200; return response

# 3
@app.route('/verifyEmail', methods=['POST'])
def verifyEmail():
    # field validation
    try: token = request.form['token'] except: response = make_response('Token field required'); response.status = 400; return response
    if token == '' or token == None: response = make_response('Token cannot be empty'); response.status = 400; return response
    
    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # search for token
    token_results = EmailVerifications.objects.filter(id = token)
    if len(token_results) == 0: response = make_response('invalid token'); response.status = 404; return response
    match = token_results[0]

    # check if token has already been used
    if match.used == True: response = make_response('used'); response.status = 409; return response

    # check if token has already expired
    if str(datetime.now()) > match.expiry_date: response = make_response('expired'); response.status = 401; return response

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
    # field validation
    try: account_id = request.form['account_id'] except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)

    # search for account by account id ... also verify validity of given account id
    match = Users.objects.filter(id = account_id)
    if len(match) == 0: response = make_response('invalid account id'); response.status = 404; return response
    account = match[0]

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
        date_of_request = current_datetime
        expiry_date = token_expiration_date
    )
    verification_details = email_verification_details.save()
    email_verification_token = verification_details.id

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
    response make_response('ok'); response.status = 200; return response

# 5
@app.route('/correctRegistrationEmail', methods=['POST'])
def correctRegistrationEmail():
    # field validation
    try: account_id = request.form['account_id'] except: response = make_response('Account ID required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response
    try: email = request.form['email'] except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('Invalid email structure'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)

    # search for account by account id ... also verify validity of given account id
    match = Users.objects.filter(id = account_id)
    if len(match) == 0: response = make_response('invalid account id'); response.status = 400; return response
    account = match[0]

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
        date_of_request = current_datetime
        expiry_date = token_expiration_date
    )
    verification_details = email_verification_details.save()
    email_verification_token = verification_details.id

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

# 6
@app.route('/recoverPassword', methods=['POST'])
def recoverPassword():
    # field validation
    try: email = request.form['email'] except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('Invalid email structure'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes())
    token_expiration_date = str(token_expiration_date_object)
    # get retry wait time in minutes
    retry_wait_minutes = token_send_on_user_request_retry_period_in_minutes()
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f'

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
        request_datetime = recovery_requests[-1].date_of_request
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
        account_id = account.id,
        email = email,
        used = False,
        device = user_device,
        ip_address = user_ip_address,
        date_of_request = current_datetime,
        expiry_date = token_expiration_date
    )
    recovery_details = password_recovery_details.save()
    password_recovery_token = recovery_details.id

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
    # field validation
    try: token = request.form['token'] except: response = make_response('Password field required'); response.status = 400; return response
    if token == '' or token == None: response = make_response('Token cannot be empty'); response.status = 400; return response
    try: password = request.form['password'] except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    if is_password_structure_valid(password) == False: response = make_response('Invalid password structure'); response.status = 400; return response

    # search for token
    token_results = PasswordRecoveries.objects.filter(id = token)
    if len(token_results) == 0: response = make_response('invalid token'); response.status = 404; return response
    match = token_results[0]

    # check if token has already been used
    if match.used == True: response = make_response('used'); response.status = 409; return response

    # check if token has already expired
    if str(datetime.now()) > match.expiry_date: response = make_response('expired'); response.status = 401; return response

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
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)

    # get user by user_id
    user = Users.objects.filter(id = user_id)[0]

    # modify user object... delete password, add subscription status
    user = json.loads(user.to_json())
    user = user_object_modification(user, current_datetime)

    # return user object minus password
    response = make_response(jsonify(user)); response.status = 200; return response

# 9
@app.route('/signout', methods=['POST'])
def signout():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # disable used access token
    token = UserAccessTokens.objects.filter(token = request.headers.get('access_token'))[0]
    UserAccessTokens.objects(id = token.id).update(active = False, signout_date = str(datetime.now()))

    # return response
    response = make_response('ok'); response.status = 200; return response

# 10
@app.route('/editProfile', methods=['POST'])
def editProfile():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response
    
    # input field validation
    try: firstname = request.form['firstname'] except: response = make_response('Firstname field required'); response.status = 400; return response
    if firstname == '' or firstname == None: response = make_response('Firstname cannot be empty'); response.status = 400; return response
    try: lastname = request.form['lastname'] except: response = make_response('Lastname field required'); response.status = 400; return response
    if lastname == '' or lastname == None: response = make_response('Lastname cannot be empty'); response.status = 400; return response
    try: username = request.form['username'] except: response = make_response('Username field required'); response.status = 400; return response
    if username == '' or username == None: response = make_response('Username cannot be empty'); response.status = 400; return response
    try: email = request.form['email'] except: response = make_response('Email field required'); response.status = 400; return response
    if email == '' or email == None: response = make_response('Email cannot be empty'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('Invalid email structure' ); response.status = 400; return response
    try: phonenumber = request.form['phonenumber'] except: response = make_response('Phonenumber field required'); response.status = 400; return response
    if phonenumber == '' or phonenumber == None: response = make_response('Phonenumber cannot be empty'); response.status = 400; return response
    try: password = request.form['password'] except: response = make_response('Password field required'); response.status = 400; return response
    if password == '' or password == None: response = make_response('Password cannot be empty'); response.status = 400; return response
    try: new_password = request.form['new_password'] except: response = make_response('New password field required'); response.status = 400; return response
    if new_password != '' and new_password != None and is_password_structure_valid(new_password) == False: response = make_response('Invalid new password structure'); response.status = 400; return response
    try: country = request.form['country'] except: response = make_response('Country field required'); response.status = 400; return response
    if country == '' or country == None: response = make_response('Country cannot be empty'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
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
            UserAccessTokens.objects(id = i.id).update(active = False, signout_date = str(datetime.now()) 
            for i in all_active_tokens if True
        ]
        return_string = return_string + ', password has been changed'
    
     # user has not supplied a new password, save existing password to password_to_save
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
            date_of_request = current_datetime
            expiry_date = token_expiration_date
        )
        verification_details = email_verification_details.save()
        email_verification_token = verification_details.id

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
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # collect payment history by user_id
    user_payment_history = Payments.objects.filter(user_id = user_id)

    # return payment history
    response = make_response(user_payment_history.to_json()); response.status = 200; return response

# market analysis functions *******************************************************************************************
# 11
@app.route('/getCurrentMarketAnalysis', methods=['POST'])
def getCurrentMarketAnalysis():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'user/admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # symbol field validation
    try: symbol = request.form['symbol'] except: response = make_response('Symbol required'); response.status = 400; return response
    if symbol == '' or symbol == None: response = make_response('Symbol cannot be empty'); response.status = 400; return response

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)

    # administration exceptions
    administration_exceptions = ['admin']

    # exempt administration exceptions from subscription checks
    if user_role not in administration_exceptions:
        # user subscription test
        user_subscription_expiration_date = Users.objects.filter(id = user_id)[0].subscription_expiry
        if current_datetime > user_subscription_expiration_date: response = make_response('not subscribed'); response.status = 403; return response

    # proceed to get current market analysis ... ie last analysis entry
    current_market_analysis = MarketAnalysis.objects.filter(symbol = symbol)[-1]

    # return current market analysis
    response = make_response(current_market_analysis.to_json()); response.status = 200; return response

# admin functions *****************************************************************************************************
# 13
@app.route('/getAllUsers', methods=['POST'])
def getAllUsers():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)

    # get user list
    all_users = Users.objects.all()

    # modify user objects... delete passwords, add subscription status
    all_users = json.loads(all_users.to_json())
    all_users = [user_object_modification(i, current_datetime) for i in all_users]

    # return user list
    response = make_response(jsonify(all_users)); response.status = 200; return response

# 14
@app.route('/getUserCountryRanking', methods=['POST'])
def getUserCountryRanking():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
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
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation
    try: start_date = request.form['start_date'] except: response = make_response('Start date field required'); response.status = 400; return response
    try: end_date = request.form['end_date'] except: response = make_response('End date field required'); response.status = 400; return response
    try: category = request.form['category'] except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    
    # get user list
    all_users = Users.objects.all()

    # return empty list if there are no users yet ... inorder to avoid errors by indexing empty list
    new_user_registration_statistics = []
    if len(all_users) == 0: response = make_response(jsonify(new_user_registration_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_users[0]['date_of_registration'][0:10] # start with first user's registration date in format yyyy-mm-dd
        end_date = str(datetime.now())[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days
    
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
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation
    try: start_date = request.form['start_date'] except: response = make_response('Start date field required'); response.status = 400; return response
    try: end_date = request.form['end_date'] except: response = make_response('End date field required'); response.status = 400; return response
    try: category = request.form['category'] except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    
    # get subscriptions list
    all_subscriptions = Payments.objects.all(purpose = 'subscription')

    # return empty list if there are no subscriptions yet ... inorder to avoid errors by indexing empty list
    new_subscribed_user_statistics = []
    if len(all_subscriptions) == 0: response = make_response(jsonify(new_subscribed_user_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_subscriptions[0]['date'][0:10] # start with first subscription's date in format yyyy-mm-dd
        end_date = str(datetime.now())[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days
    
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
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation
    try: account_id = request.form['account_id'] except: response = make_response('Account ID field required'); response.status = 400; return response
    if account_id == '' or account_id == None: response = make_response('Account ID cannot be empty'); response.status = 400; return response

    # collect payment history by user_id
    user_payment_history = Payments.objects.filter(user_id = account_id)

    # return payment history
    response = make_response(user_payment_history.to_json()); response.status = 200; return response

# 19
@app.route('/searchForUser', methods=['POST'])
def searchForUser():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation
    try: search_query = request.form['search_query'] except: response = make_response('Search query field required'); response.status = 400; return response
    if search_query == '' or search_query == None: response = make_response('Search query cannot be empty'); response.status = 400; return response

    # get current datetime
    current_datetime_object = datetime.now()
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

    # return user list
    response = make_response(jsonify(user_results)); response.status = 200; return response

# 20
@app.route('/getUserCount', methods=['POST'])
def getUserCount():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation
    try: start_date = request.form['start_date'] except: response = make_response('Start date field required'); response.status = 400; return response
    try: end_date = request.form['end_date'] except: response = make_response('End date field required'); response.status = 400; return response
    try: category = request.form['category'] except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    
    # get user list
    all_users = Users.objects.all()

    # return empty list if there are no users yet ... inorder to avoid errors by indexing empty list
    user_count_statistics = []
    if len(all_users) == 0: response = make_response(jsonify(user_count_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_users[0]['date_of_registration'][0:10] # start with first user's registration date in format yyyy-mm-dd
        end_date = str(datetime.now())[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days
    
    # list of days
    list_of_days = [str(datetime.strptime(start_date, date_format) + timedelta(days=i)) for i in range(date_difference_in_days)]

    # create user count statistics
    user_count_statistics = [
        {'date': i[0:10], 'users': len([
            z for z in all_users if 
            i[0:10] <= z.date_of_registration[0:10]
        ])}
        for i in list_of_days if True
    ]

    # return statistics
    response = make_response(jsonify(user_count_statistics)); response.status = 200; return response

# 21
@app.route('/getUserSubscriptionStatistics', methods=['POST'])
def getUserSubscriptionStatistics():
    # check user access token's validity
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # input field validation
    try: start_date = request.form['start_date'] except: response = make_response('Start date field required'); response.status = 400; return response
    try: end_date = request.form['end_date'] except: response = make_response('End date field required'); response.status = 400; return response
    try: category = request.form['category'] except: response = make_response('Category field required'); response.status = 400; return response
    if category == '' or category == None: response = make_response('Category cannot be empty'); response.status = 400; return response
    
    # get subscriptions list
    all_subscriptions = Payments.objects.all(purpose = 'subscription')

    # return empty list if there are no subscriptions yet ... inorder to avoid errors by indexing empty list
    subscribed_user_statistics = []
    if len(all_subscriptions) == 0: response = make_response(jsonify(subscribed_user_statistics)); response.status = 200; return response

    # start and end days if they were'nt given on as input
    if (start_date == '' or start_date == None) or (end_date == '' or end_date == None):
        start_date = all_subscriptions[0]['date'][0:10] # start with first subscription's date in format yyyy-mm-dd
        end_date = str(datetime.now())[0:10]

    # date format
    date_format = '%Y-%m-%d'

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days
    
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
    access_token_status, user_id, user_role = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get current datetime
    current_datetime_object = datetime.now()
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
        'users_not_verified': len([i for i in all_users if i['verified'] == False])
    }

    # return statistics
    response = make_response(jsonify(user_metrics)); response.status = 200; return response

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
    # app.run(host=os.environ.get("BACKEND_HOST", "0.0.0.0"), port=5000) # for use in docker
    # from waitress import serve
    # serve(app, host='0.0.0.0') # use waitress