import requests
import json
import os
from collections import deque
from user_subscription_check import validate_subscription
from settings import platform_name, user_roles_exempted_from_subscribing

# get platform name
platform_brand_name = platform_name()

# telegram token
token = os.environ.get('TELEGRAM_BOT_TOKEN')

# api url
api_url = 'https://api.telegram.org/bot{}/'.format(token)

# send telegram message *********************************************************************************************************
def send_message(chat_id, message):
    message_sent = False

    # keep trying to send the message until successful
    while message_sent == False:
        try:
            request_url = api_url + 'sendMessage?chat_id={}&text={}'.format(chat_id, message)
            requests.get(request_url, verify=True) # verify=True to verify SSL certificate, ie to ensure end to end encryption
            message_sent = True
        except:
            print('\n\nSomething went wrong while trying to send a Telegram message. Trying again ...\n\n')
# *******************************************************************************************************************************

# get message updates ***********************************************************************************************************
def get_updates():
    while True:
        try:
            request_url = api_url + "getUpdates" # removed long polling (defaults to 0 seconds): ?timeout=100
            request_result = requests.get(request_url, verify=True) # verify=True to verify SSL certificate, ie to ensure end to end encryption
            result = json.loads(request_result.content)
            messages = result['result']
            break
        except:
            print('\n\nSomething went wrong while trying to check for new Telegram messages. Retrying...\n\n')

    return messages
# *******************************************************************************************************************************

# user submitted telegram connect code search ***********************************************************************************
def search_for_user_submitted_telegram_connect_code(user_telegram_connect_code):
    # retrieve messages
    messages = get_updates()

    # get all messages containing the user's telegram connect code
    messages_containing_user_telegram_code = [i for i in messages if str(i['message']['text']) == user_telegram_connect_code]

    # if code has been found
    if len(messages_containing_user_telegram_code) > 0:
        # get the first message received containing that code
        first_message_received_containing_the_code = messages_containing_user_telegram_code[0]

        # set code found to true
        code_found = True

        # get the matching message's id
        message_id = str(first_message_received_containing_the_code['update_id'])

        # get the sender's telegram id
        sender_id = str(first_message_received_containing_the_code['message']['from']['id'])
    
    # if the code has not been found
    else:
        # set code found to false
        code_found = False

        # set sender id to None
        sender_id = None

    # return code found status and the sender's telegram id
    return code_found, sender_id
# *******************************************************************************************************************************

# user successful telegram connection message ***********************************************************************************
def send_user_successful_telegram_connection_message(user_telegram_id, user_firstname):
    # construct message
    message = "Hello {}. Your connection was a success. Thank you for choosing {}.".format(user_firstname, platform_brand_name)
    
    # send message
    send_message(user_telegram_id, message)
# *******************************************************************************************************************************

# trade signals telegram alerts *************************************************************************************************
def send_trade_signal_alerts_via_telegram(predictions_string, users_with_their_telegram_connected):
    # loop through users who connected their telegram *****************************************************************
    for user in users_with_their_telegram_connected:
        # get user telegram id
        user_telegram_id = user['telegram_id']

        # get user role
        user_role = user['role']

        # get user subscription status
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)

        # if a user is subscribed or is exempted from subscribing because of their role *********************
        if user_subscribed == True or user_role in user_roles_exempted_from_subscribing():
            # send a telegram trade signal(s) alert
            send_message(user_telegram_id, predictions_string)
        # ***************************************************************************************************
    # *****************************************************************************************************************
# *******************************************************************************************************************************

# account role change telegram notification *************************************************************************************
def send_account_role_change_telegram_notification(telegram_id, username, firstname, lastname, old_role, new_role): # roles = user / admin / free user
    # notification text ***********************************************************************************************
    if old_role == 'admin' and new_role == 'user':
        notification_text = "Your account's access level has been downgraded. You now have ordinary user level access only."
    elif old_role == 'admin' and new_role == 'free user':
        notification_text = "Your account's access level has been downgraded. You now have ordinary user level access only. However, you have been given free access until further notice. We hope you enjoy your free access period and find it valuable. Happy trading."
    elif ((old_role == 'user' or old_role == 'free user') and new_role == 'admin') or (old_role == 'admin' and new_role == 'admin'):
        notification_text = 'Your account now has admin access.'
    elif (old_role == 'free user' and new_role == 'user') or (old_role == 'user' and new_role == 'user'):
        notification_text = 'Your account no longer has free access. We really hope you enjoyed your free access period and found it valuable.'
    elif (old_role == 'user' and new_role == 'free user') or (old_role == 'free user' and new_role == 'free user'):
        notification_text = 'Your account has been given free access until further notice. We hope you enjoy your free access period and find it valuable. Happy trading.'
    # *****************************************************************************************************************

    # message content text ********************************************************************************************
    message_content_text = """
Hi {firstname},

{notification_text}

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # send crafted message
    send_message(telegram_id, message_content_text)
# *******************************************************************************************************************************

# payment confirmation telegram notification ************************************************************************************
def send_payment_confirmation_telegram_notification(telegram_id, username, firstname, lastname, amount, subcription, subscription_package):
    # notification text ***********************************************************************************************
    if subcription == True:
        notification_text = f'Your payment of ${amount} for our {subscription_package} was successful. Thank you for your continued support.' 
    else:
        notification_text = f'Your payment of ${amount} was successful. Thank you for your continued support.'
    # *****************************************************************************************************************

    # message content text ********************************************************************************************
    message_content_text = """
Hi {firstname},

{notification_text}

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # send crafted email
    send_message(telegram_id, message_content_text)
# *******************************************************************************************************************************

# subscription expiration telegram notification *********************************************************************************
def send_subscription_expiration_telegram_notification(telegram_id, username, firstname, lastname, free_trial, expired, days_till_expiry):
    # notification text ***********************************************************************************************
    if free_trial == True and expired == False:
        notification_text = f'Your free trial will be expiring in {days_till_expiry} days.' 
    elif free_trial == True and expired == True:
        notification_text = f'Your free trial has expired. We really hope you enjoyed your free access period and found it valuable.' 
    elif free_trial == False and expired == False:
        notification_text = f'Your subscription will be expiring in {days_till_expiry} days. To avoid service interruption, you need to top up your subscription.' 
    elif free_trial == False and expired == True:
        notification_text = f'Your subscription has expired. We really hope you found your subscription period valuable.' 
    # *****************************************************************************************************************

    # message content text ********************************************************************************************
    message_content_text = """
Hi {firstname},

{notification_text}

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # send crafted email
    send_message(telegram_id, message_content_text)
# *******************************************************************************************************************************