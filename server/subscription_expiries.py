from database import init_db
from models import Users
import json
from collections import deque
from user_subscription_check import validate_subscription
from settings import get_number_of_days_from_expiry_to_send_free_trial_expiring_soon_alert, get_number_of_days_from_expiry_to_send_subscription_expiring_soon_alert
import time
from emails import send_subscription_expiration_notification_email
from telegram import send_subscription_expiration_telegram_notification

# initialize database connection in this module *******************************************************************************************
init_db()
# *****************************************************************************************************************************************

# always on loop ... will pause for 1 hour at its end, meaning it will be running hourly **************************************************
print('\n\nSubscription expiries module on.')
while True:
    # get all email verified users **********************************************************************************************
    all_users_with_their_emails_verified = Users.objects.filter(verified = True)
    all_users_with_their_emails_verified = json.loads(all_users_with_their_emails_verified.to_json())
    all_users_with_their_emails_verified = deque(all_users_with_their_emails_verified) # conversion to deque array for faster looping
    # ***************************************************************************************************************************

    # loop through users ********************************************************************************************************
    for user in all_users_with_their_emails_verified:
        # user subscription status and info check *********************************************************************
        user_subscribed, subcription_expiry_date, on_free_trial, days_till_expiry = validate_subscription(user)
        # *************************************************************************************************************

        # check if user's subscription is about to expire *************************************************************
        if (
            # free trial about to expire
            (user_subscribed == True and on_free_trial == True and user['subscription_expiring_soon_notification_issued'] != True and days_till_expiry <= get_number_of_days_from_expiry_to_send_free_trial_expiring_soon_alert()) or
            # paid subscription about to expire
            (user_subscribed == True and on_free_trial == False and user['subscription_expiring_soon_notification_issued'] != True and days_till_expiry <= get_number_of_days_from_expiry_to_send_subscription_expiring_soon_alert())
        ): user_subscription_is_about_to_expire = True
        else: user_subscription_is_about_to_expire = False
        # *************************************************************************************************************

        # check if user's subscription has expired ********************************************************************
        if (
            # expired
            (user_subscribed == False and user['subscription_expired_notification_issued'] != True)
        ): user_subscription_has_expired = True
        else: user_subscription_has_expired = False
        # *************************************************************************************************************

        # alert *******************************************************************************************************
        if user_subscription_is_about_to_expire == True or user_subscription_has_expired == True:
            # via email *************************************************************************************
            send_subscription_expiration_notification_email(
                user['email'], # email
                user['username'], # username
                user['firstname'], # firstname
                user['lastname'], # lastname
                on_free_trial, # free trial ... whether the user is still on free trial or is now on a paid subscription
                not user_subscribed, # expired ... whether the user's free trial / paid subscription has expired or not
                days_till_expiry # days till free trial / subscription expiry
            )
            # ***********************************************************************************************
            # via telegram **********************************************************************************
            if user['telegram_connected'] == True:
            send_subscription_expiration_telegram_notification(
                user['telegram_id'], # telegram id
                user['username'], # username
                user['firstname'], # firstname
                user['lastname'], # lastname
                on_free_trial, # free trial ... whether the user is still on free trial or is now on a paid subscription
                not user_subscribed, # expired ... whether the user's free trial / paid subscription has expired or not
                days_till_expiry # days till free trial / subscription expiry
            )
            # ***********************************************************************************************
        # *************************************************************************************************************

        # show that user has received this alert **********************************************************************
        # about to expire alert *****************************************************************************
        if user_subscription_is_about_to_expire: 
            Users.objects(id = user['_id']['$oid']).update(subscription_expiring_soon_notification_issued = True)
        # ***************************************************************************************************
        # expired alert *************************************************************************************
        if user_subscription_has_expired: 
            Users.objects(id = user['_id']['$oid']).update(subscription_expired_notification_issued = True)
        # ***************************************************************************************************
        # *************************************************************************************************************
    # ***************************************************************************************************************************

    # pause loop for 1 hour *****************************************************************************************************
    time.sleep(3600) # there's 3600 seconds in an hour
    # ***************************************************************************************************************************
# *****************************************************************************************************************************************