# imports
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
from user_agents import parse
from datetime import datetime, timedelta
import requests
from database import init_db
from models import  Users, EmailVerifications, UserAccessTokens, PasswordRecoveries, MarketAnalysisPayments, LoginTrials
from encryption import encrypt_password, verify_encrypted_password
from emails import send_registration_email_confirmation, send_password_recovery_email, send_email_change_confirmation
from settings import verification_token_expiration_minutes, access_token_expiration_days, token_send_on_user_request_retry_period_in_minutes

# Flask stuff
app = Flask(__name__)
app.debug = True

# Cross Origin Stuff
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['CORS_HEADERS'] = 'Access-Control-Allow-Origin'
# app.config['CORS_RESOURCES'] = {r"/*": {"origins": "*"}}
cors = CORS(app)

# frontend url
frontend_url = 'http://localhost:3000' # development server

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
def check_user_access_token_validity(request_data):
    try:
        # get user access token
        user_access_token = request.form['user_access_token']
        # get information on user's browsing device
        user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request_data)
        # check token's validity while trying to retrieve the user's system id
        token_details = AccessTokens.objects.filter(
            id = user_access_token, 
            active = True, 
            user_browsing_agent = user_browsing_agent
        )[0]
        # get user id
        user_id = token_details.user_id
        # get current date and time
        current_datetime = str(datetime.now())
        # get access token status
        if token_details.active == False:
            access_token_status = 'Access token disabled via signout'
        elif current_datetime > token_details.expiry_date:
            access_token_status = 'Access token expired'
        else:
            access_token_status = 'ok'
            # show that access token was last used now
            AccessTokens.objects(id = user_access_token).update(last_used_on_date = current_datetime)
        # return access_token_status, user_id
        return access_token_status, user_id
    except:
        return 'Not authorized', None

# user functions ******************************************************************************************************
@app.route('/signup', methods=['POST'])
def signup():
    # check if username is already in use
    if len(Users.objects.filter(username = request.form['username'])) > 0: return 'username in use'

    # check if email is already in use
    if len(Users.objects.filter(email = request.form['email'])) > 0: return 'email in use'

    # check if phonenumber is already in use
    if len(Users.objects.filter(phonenumber = request.form['phonenumber'])) > 0: return 'phonenumber in use'

    # encrypt submitted password
    password = request.form['password']
    password = encrypt_password(password)
    
    # register new user and retrieve account id
    user_details = Users(
        firstname = request.form['firstname'],
        lastname = request.form['lastname'],
        username = request.form['username'],
        email = request.form['email'],
        phonenumber = request.form['phonenumber'],
        password = password,
        country = request.form['country'],
        date_of_registration = str(datetime.now())
        verified = False,
        subscribed = False,
        subscription_date = '',
        subscription_expiry = '',
        role = 'User',
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
        email = request.form['email'],
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
        request.form['email'], 
        request.form['username'], 
        email_verification_token, 
        token_expiration_date
    ) # inputs: user_email, username, verification_token, token_expiration_date

    # return account id
    return account_id

@app.route('/signin', methods=['POST'])
def signin():
    # get submitted details
    email_or_username = request.form['email_or_username']
    password = request.form['password']

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
        return 'email or username not registered'

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
        return 'incorrect details entered'

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
        return 'banned'

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
    user_access_token = generate_access_token + '.' + token_id
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
    return user_access_token
    
@app.route('/verifyEmail', methods=['POST'])
def verifyEmail():
    # search for token
    token_results = EmailVerifications.objects.filter(id = request.form['token'])
    if len(token_results) == 0: return 'invalid token'
    match = token_results[0]

    # check if token has already been used
    if match.used == True: return 'used'

    # check if token has already expired
    if str(datetime.now()) > match.expiry_date: return 'expired'

    # verify user account
    Users.objects(id = match.account_id).update(verified = True)

    # mark token as used
    EmailVerifications.objects(id = request.form['token']).update(used = True)

    return 'ok'

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
    if len(match) == 0: return 'invalid account id'
    account = match[0]

    # check if email has already been verified
    if account.verified == True: return 'email already verified'

    # proceed to create email verification token
    email_verification_details = EmailVerifications(
        account_id = request.form['account_id'],
        email = account.email,
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

@app.route('/correctRegistrationEmail', methods=['POST'])
def correctRegistrationEmail():
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
    Users.objects(id = request.form['account_id']).update(email = request.form['email'])
    account = Users.objects.filter(id = request.form['account_id'])[0]

    # proceed to create email verification token
    email_verification_details = EmailVerifications(
        account_id = request.form['account_id'],
        email = account.email,
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
    match = Users.objects.filter(email = request.form['email'])
    if len(match) == 0: return 'email not registered'
    account = match[0]

    # check if account has been banned
    if account.banned == True: return 'banned'

    # check time of last active password recovery request by user
    requests = PasswordRecoveries.objects.filter(email = request.form['email'], used = False)
    if len(requests) > 0:
        # get request time
        request_datetime = requests[0].date_of_request
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
        email = request.form['email'],
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

@app.route('/getUserDetailsByAccessToken', methods=['POST'])
def getUserDetailsByAccessToken():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

@app.route('/signout', methods=['POST'])
def signout():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

@app.route('/editProfile', methods=['POST'])
def editProfile():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

@app.route('/verifyEmailChangePassword', methods=['POST'])
def verifyEmailChangePassword():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

@app.route('/getUserPaymentHistory', methods=['POST'])
def getUserPaymentHistory():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status
    
    
# market analysis functions *******************************************************************************************
@app.route('/getMarketAnalysis', methods=['POST'])
def getMarketAnalysis():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

# admin functions *****************************************************************************************************
@app.route('/getAllUsers', methods=['POST'])
def getAllUsers():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

@app.route('/getUserCountryRanking', methods=['POST'])
def getUserCountryRanking():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

@app.route('/getDailyUserRegistrationChart', methods=['POST'])
def getDailyUserRegistrationChart():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

@app.route('/getDailySubscribedUserCountChart', methods=['POST'])
def getDailySubscribedUserCountChart():
    # check user access token's validity
    access_token_status, user_id = check_user_access_token_validity(request)
    if access_token_status != 'ok':  access_token_status

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
    # app.run(host=os.environ.get("BACKEND_HOST", "0.0.0.0"), port=5000) # for use in docker
    # from waitress import serve
    # serve(app, host='0.0.0.0') # use waitress