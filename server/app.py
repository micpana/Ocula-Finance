# imports
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS, cross_origin
from user_agents import parse
from datetime import datetime
import requests
from database import init_db
from models import  Users, EmailVerifications, UserAccessTokens, PasswordRecoveries, MarketAnalysisPayments
from encryption import encrypt_password, verify_encrypted_password

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

# function for checking a user access token's validity
def check_user_access_token_validity(request_data):
    try:
        # get user access token
        user_access_token = request.form['user_access_token']
        # get information on user's browsing device
        user_browsing_agent, user_os, user_device, user_ip_address, user_browser = information_on_user_browsing_device(request_data)
        # check token's validity while trying to retrieve the user's system id
        user_id = AccessTokens.objects.filter(
            id = user_access_token, 
            active = True, 
            user_browsing_agent = user_browsing_agent
        )[0].user_id
        # return access_token_status, user_id
        return access_token_status, user_id
    except:
        return 'Not authorized'

# user functions ******************************************************************************************************
@app.route('/signup', methods=['POST'])
def signup():
    # check if username is already in use
    if len(Users.objects.filter(username = request.form['username'])) > 0: return 'username in use'

    # check if email is already in use
    if len(Users.objects.filter(email = request.form['email'])) > 0: return 'email in use'

    # encrypt submitted password
    password = request.form['password']
    password = encrypt_password(password)
    
    # register new user
    user_details = Users(
        firstname = request.form['firstname'],
        lastname = request.form['lastname'],
        username = request.form['username'],
        email = request.form['email'],
        phonenumber = request.form['phonenumber'],
        password = password,
        country = request.form['country']
    )
    user_details.save()

    # send user email verification

    return 'ok'

@app.route('/signin', methods=['POST'])
def signin():
    # get submitted details
    email_or_username = request.form['email_or_username']
    password = request.form['password']

    # get user with matching email
    matches_by_email = Users.objects.filter(email = email_or_username)
    if len(matches_by_email) > 0: 
        match = matches_by_email[0]

    # get user with matching username
    matches_by_username = Users.objects.filter(username = email_or_username)
    if len(matches_by_username) > 0:
        match = matches_by_username[0]

    # no matches found
    if len(matches_by_email) == 0 and len(matches_by_username) == 0:
        return 'email or username not registered'

    # see if password is a match
    user_encrypted_password = match.password
    is_password_a_match = verify_encrypted_password(password, user_encrypted_password)

    # create and return user access token
    

@app.route('/verifyEmail', methods=['POST'])
def verifyEmail():

@app.route('/recoverPassword', methods=['POST'])
def recoverPassword():

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