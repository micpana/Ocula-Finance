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
from emails import send_registration_email_confirmation, send_password_recovery_email, send_email_change_confirmation
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
    user_browsing_agent = request.headers.get('User-Agent')
    user_agent_parsed = parse(user_browsing_agent)
    # get user's operating system
    user_os = user_agent_parsed.os.family
    # get user's device
    user_device = user_agent_parsed.device.family
    # get user's ip address
    user_ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    # get user's browser
    user_browser = user_agent_parsed.browser.family

    return user_browsing_agent, user_os, user_device, user_ip_address, user_browser

# function for saving login trials
def save_login_trials(account_id, email, device, ip_address, date_and_time, status):
    trial_details = LoginTrials(
        account_id = account_id,
        email = email,
        device = device,
        ip_address = ip_address,
        date_and_time = date_and_time,
        status = status
    )
    trial_details.save()

    return 'ok'

# function for checking a user access token's validity
def check_user_access_token_validity(request_data, expected_user_role):
    try:
        # get user access token
        user_access_token = request.headers.get('access_token')
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
        else:
            # check if user account's role matches expected user role
            if user_role != expected_user_role: return 'Not authorized to access this'
            # proceed since everything checks out
            access_token_status = 'ok'
            # show that access token was last used now
            AccessTokens.objects(id = user_access_token).update(last_used_on_date = current_datetime)
        # return access_token_status, user_id
        return access_token_status, user_id
    except:
        return 'Invalid token', None

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

# index
@app.route('/', methods=['POST', 'GET'])
def index():
    response = make_response('Not authorized')
    response.status = 401
    return response

# user functions ******************************************************************************************************
@app.route('/signup', methods=['POST'])
def signup():
    # input field validation
    try: firstname = request.form['firstname'] except: response = make_response('Firstname field required'); response.status = 400; return response
    try: lastname = request.form['lastname'] except: response = make_response('Lastname field required'); response.status = 400; return response
    try: username = request.form['username'] except: response = make_response('Username field required'); response.status = 400; return response
    try: email = request.form['email'] except: response = make_response('Email field required'); response.status = 400; return response
    if is_email_structure_valid(email) == False: response = make_response('Invalid email structure') ; response.status = 400; return response
    try: phonenumber = request.form['phonenumber'] except: response = make_response('Phonenumber field required'); response.status = 400; return response
    try: password = request.form['password'] except: response = make_response('Password field required'); response.status = 400; return response
    if is_password_structure_valid(password) == False: response = make_response('Invalid password structure'); response.status = 400; return response
    try: country = request.form['country'] except: response = make_response('Country field required'); response.status = 400; return response

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
        subscribed = False,
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
        email_verification_token, 
        token_expiration_date
    ) # inputs: user_email, username, verification_token, token_expiration_date

    # return account id
    return response = make_response(account_id); response.status = 201; return response

@app.route('/signin', methods=['POST'])
def signin():
    # input field validation
    try: email_or_username = request.form['email_or_username'] except: response = make_response('Email or username field required'); response.status = 400; return response
    try: password = request.form['password'] except: response = make_response('Password field required'); response.status = 400; return response

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
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
            user_device, 
            user_ip_address, 
            current_datetime, 
            False
        ) # input: account_id, email, device, ip_address, date_and_time, successful (bool)
        response = make_response('email or username not registered'); response.status = 404; return response

    # see if password is a match
    user_encrypted_password = match.password
    is_password_a_match = verify_encrypted_password(password, user_encrypted_password)
    if is_password_a_match == False: 
        # save login trial
        save_login_trials(
            match.id, 
            match.email, 
            user_device, 
            user_ip_address, 
            current_datetime, 
            False
        ) # input: account_id, email, device, ip_address, date_and_time, successful (bool)
        response = make_response('incorrect details entered'); response.status = 401; return response

    # check if account is banned or not
    if match.banned == True: 
        # save login trial
        save_login_trials(
            match.id, 
            match.email, 
            user_device, 
            user_ip_address, 
            current_datetime, 
            False
        ) # input: account_id, email, device, ip_address, date_and_time, successful (bool)
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
        user_device, 
        user_ip_address, 
        current_datetime, 
        False
    ) # input: account_id, email, device, ip_address, date_and_time, successful (bool)

    # return user_access_token
    response = make_response(user_access_token); response.status = 200; return response
    
@app.route('/verifyEmail', methods=['POST'])
def verifyEmail():
    # search for token
    token_results = EmailVerifications.objects.filter(id = request.form['token'])
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
        Users.objects(id = match.account_id).update(email = match.email)

    # mark token as used
    EmailVerifications.objects(id = request.form['token']).update(used = True)

    response = make_response('ok'); response.status = 200; return response

@app.route('/resendEmailVerification', methods=['POST'])
def resendEmailVerification():
    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes)
    token_expiration_date = str(token_expiration_date_object)

    # search for account by account id ... also verify validity of given account id
    match = Users.objects.filter(id = request.form['account_id'])
    if len(match) == 0: response = make_response('invalid account id'); response.status = 404; return response
    account = match[0]

    # check if email has already been verified
    if account.verified == True: response = make_response('email already verified'); response.status = 409; return response

    # proceed to create email verification token
    email_verification_details = EmailVerifications(
        account_id = request.form['account_id'],
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
        email_verification_token, 
        token_expiration_date
    ) # inputs: user_email, username, verification_token, token_expiration_date

    response make_response('ok'); response.status = 200; return response

@app.route('/correctRegistrationEmail', methods=['POST'])
def correctRegistrationEmail():
    # field validation
    try: email = request.form['email'] except: return 'Email field required'
    if is_email_structure_valid(email) == False: return 'Invalid email structure' 

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes)
    token_expiration_date = str(token_expiration_date_object)

    # search for account by account id ... also verify validity of given account id
    match = Users.objects.filter(id = request.form['account_id'])
    if len(match) == 0: return 'invalid account id'
    account = match[0]

    # check if email has already been verified
    if account.verified == True: return 'email already verified'

    # notify of email's non availability even if it is not verified
    if account.verified == False: return 'email already registered'

    # update account email and gather updated account information
    Users.objects(id = request.form['account_id']).update(email = email)
    account = Users.objects.filter(id = request.form['account_id'])[0]

    # proceed to create email verification token
    email_verification_details = EmailVerifications(
        account_id = request.form['account_id'],
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
        email_verification_token, 
        token_expiration_date
    ) # inputs: user_email, username, verification_token, token_expiration_date

    return 'ok'

@app.route('/recoverPassword', methods=['POST'])
def recoverPassword():
    # field validation
    try: email = request.form['email'] except: return 'Email field required'
    if is_email_structure_valid(email) == False: return 'Invalid email structure' 

    # get user browsing device information
    user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request)

    # get current datetime
    current_datetime_object = datetime.now()
    current_datetime = str(current_datetime_object)
    # calculate verification token expiration date
    token_expiration_date_object = current_datetime_object + timedelta(minutes = verification_token_expiration_minutes)
    token_expiration_date = str(token_expiration_date_object)
    # get retry wait time in minutes
    retry_wait_minutes = token_send_on_user_request_retry_period_in_minutes()
    # date format
    date_format = '%Y-%m-%d %H:%M:%S.%f'

    # search for account by email
    match = Users.objects.filter(email = email)
    if len(match) == 0: return 'email not registered'
    account = match[0]

    # check if account has been banned
    if account.banned == True: return 'banned'

    # check time of last active password recovery request by user
    recovery_requests = PasswordRecoveries.objects.filter(email = email, used = False)
    if len(recovery_requests) > 0:
        # get request time
        request_datetime = recovery_requests[0].date_of_request
        # calculate end-datetime for waiting period
        retry_wait_ending_time_object = datetime.strptime(request_datetime, date_format) + timedelta(minutes = retry_wait_minutes)
        # check if last request was made outside of the retry wait period 
        if retry_wait_ending_time_object > current_datetime_object: 
            # remaining time in minutes
            time_difference = retry_wait_ending_time_object - current_datetime_object
            remaining_time_in_minutes = time_difference.total_seconds() / 60
            return 'try again in ' + str(remaining_time_in_minutes) + ' minutes.'

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
        password_recovery_token, 
        token_expiration_date
    ) # inputs: user_email, username, recovery_token, token_expiration_date

    return 'ok'

@app.route('/setNewPassword', methods=['POST'])
def setNewPassword():
    # field validation
    try: password = request.form['password'] except: return 'Password field required'
    if is_password_structure_valid(password) == False: return 'Invalid password structure'

    # search for token
    token_results = PasswordRecoveries.objects.filter(id = request.form['token'])
    if len(token_results) == 0: return 'invalid token'
    match = token_results[0]

    # check if token has already been used
    if match.used == True: return 'used'

    # check if token has already expired
    if str(datetime.now()) > match.expiry_date: return 'expired'

    # encrypt submitted password
    password = encrypt_password(password)

    # set new password to user account
    Users.objects(id = match.account_id).update(password = password)

    # mark token as used
    PasswordRecoveries.objects(id = request.form['token']).update(used = True)

    return 'ok'

@app.route('/getUserDetailsByAccessToken', methods=['POST'])
def getUserDetailsByAccessToken():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'user') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get user by user_id
    user = Users.objects.filter(id = user_id)[0]

    # remove password from details
    user = json.loads(user.to_json())
    del user['password']

    # return user object minus password
    return jsonify(user)

@app.route('/signout', methods=['POST'])
def signout():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'user') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # disable used access token
    token = UserAccessTokens.objects.filter(token = request.headers.get('access_token'))[0]
    UserAccessTokens.objects(id = token.id).update(active = False, signout_date = str(datetime.now()))

    return 'ok'

@app.route('/editProfile', methods=['POST'])
def editProfile():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'user') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response
    
    # input field validation
    try: firstname = request.form['firstname'] except: return 'Firstname field required'
    try: lastname = request.form['lastname'] except: return 'Lastname field required'
    try: username = request.form['username'] except: return 'Username field required'
    try: email = request.form['email'] except: return 'Email field required'
    if is_email_structure_valid(email) == False: return 'Invalid email structure' 
    try: phonenumber = request.form['phonenumber'] except: return 'Phonenumber field required'
    try: password = request.form['password'] except: return 'Password field required'
    try: new_password = request.form['new_password'] except: return 'New password field required'
    if is_password_structure_valid(new_password) == False: return 'Invalid password structure'
    try: country = request.form['country'] except: return 'Country field required'

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
    if is_password_a_match == False: return 'incorrect password'

    # check if username is already in use ... if user has changed field
    if user.username != username and len(Users.objects.filter(username = username)) > 0: return 'username in use'

    # check if email is already in use ... if user has changed field
    if user.email != email and len(Users.objects.filter(email = email)) > 0: return 'email in use'

    # check if phonenumber is already in use ... if user has changed field
    if user.phonenumber != phonenumber and len(Users.objects.filter(phonenumber = phonenumber)) > 0: return 'phonenumber in use'

    # check if new password and existing password are a match
    new_password_matches_existing = verify_encrypted_password(new_password, user_encrypted_password)
    if new_password_matches_existing == True: return 'new password matches existing'

    # check if user has changed password ... if so, save new encrypted password to password_to_save
    if new_password != '' and new_password_matches_existing == False:
        password_to_save = encrypt_password(new_password)
    else: password_to_save = user_encrypted_password # no password change

    # update account details
    Users.objects(id = user_id).update(
        firstname = firstname,
        lastname = lastname,
        username = username,
        phonenumber = phonenumber,
        password = password_to_save,
        country = country,
    )

    # initialize return string
    return_string = 'ok'

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
            email_verification_token, 
            token_expiration_date
        ) # inputs: user_email, username, verification_token, token_expiration_date

        # add more context to return string
        return_string = return_string + ', email verification sent.'

    # return return_string
    return return_string

@app.route('/getUserPaymentHistory', methods=['POST'])
def getUserPaymentHistory():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'user') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # collect payment history by user_id
    user_payment_history = Payments.objects.filter(user_id = user_id)

    # return payment history
    return user_payment_history.to_json()
    
# market analysis functions *******************************************************************************************
@app.route('/getCurrentMarketAnalysis', methods=['POST'])
def getCurrentMarketAnalysis():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'user') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # symbol field validation
    try: symbol = request.form['symbol'] except: return 'Symbol required'

    # get current market analysis ... ie last analysis entry
    current_market_analysis = MarketAnalysis.objects.filter(symbol = symbol)[-1]

    # return current market analysis
    return current_market_analysis.to_json()

# admin functions *****************************************************************************************************
@app.route('/getAllUsers', methods=['POST'])
def getAllUsers():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get user list
    all_users = Users.objects.all()

    # return user list
    return all_users.to_json()

@app.route('/getUserCountryRanking', methods=['POST'])
def getUserCountryRanking():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'admin') # request data, expected user role
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
    return jsonify(user_country_list)

@app.route('/getDailyUserRegistrationStatistics', methods=['POST'])
def getDailyUserRegistrationStatistics():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get user list
    all_users = Users.objects.all()

    # create daily user registration statistics
    processed_days = []
    daily_user_registration_statistics = [
        {'date': i.date_of_registration[0:10], 'users': len([z for z in all_users if z.date_of_registration[0:10] == i.date_of_registration[0:10]])}
        for i in all_users if i.date_of_registration[0:10] not in processed_days and not processed_days.append(i.date_of_registration[0:10])
    ]

    # return statistics
    return jsonify(daily_user_registration_statistics)

@app.route('/getDailySubscribedUserCountStatistics', methods=['POST'])
def getDailySubscribedUserCountStatistics():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request, 'admin') # request data, expected user role
    if access_token_status != 'ok':  response = make_response(access_token_status); response.status = 401; return response

    # get subscriptions list
    all_subscriptions = Payments.objects.all(purpose = 'subscription')

    # return empty list if there are no subscriptions yet ... inorder to avoid errors by indexing empty list
    daily_subscribed_user_statistics = []
    if len(all_subscriptions) == 0: return jsonify(daily_subscribed_user_statistics)

    # date format
    date_format = '%Y-%m-%d'

    # start and end days
    start_date = all_subscriptions[0]['date'][0:10] # start with first subscription's date in format yyyy-mm-dd
    end_date = str(datetime.now())[0:10]

    # difference between dates in days
    date_difference_in_days = datetime.strptime(end_date, date_format) - datetime.strptime(start_date, date_format)
    date_difference_in_days = date_difference_in_days.days
    
    # list of days
    list_of_days = [str(datetime.strptime(start_date, date_format) + timedelta(days=i)) for i in range(date_difference_in_days)]

    # create daily subscribed user statistics
    daily_subscribed_user_statistics = [
        {'date': i[0:10], 'users': len([
            z for z in all_subscriptions if 
            i >= z.date[0:10] and 
            i < z.expiry_date
        ])}
        for i in list_of_days if True
    ]

    # return statistics
    return jsonify(daily_subscribed_user_statistics)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
    # app.run(host=os.environ.get("BACKEND_HOST", "0.0.0.0"), port=5000) # for use in docker
    # from waitress import serve
    # serve(app, host='0.0.0.0') # use waitress