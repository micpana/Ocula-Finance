from pytz import timezone
from datetime import datetime, timedelta
from settings import get_number_of_free_trial_days, system_timezone

# function to check if a user has an active subscription or not ***************************************************************************
def validate_subscription(user):
    # get current datetime ******************************************************************************************************
    current_datetime_object = datetime.now(timezone(system_timezone()))
    current_datetime = str(current_datetime_object)
    # ***************************************************************************************************************************

    # date format ***************************************************************************************************************
    date_format = '%Y-%m-%d %H:%M:%S.%f%z'
    # ***************************************************************************************************************************

    # user telegram verification date *******************************************************************************************
    user_telegram_verification_date = user['date_of_telegram_verification']
    # ***************************************************************************************************************************

    # user subscription expiry date *********************************************************************************************
    user_subscription_expiration_date = user['subscription_expiry']
    # ***************************************************************************************************************************
    
    # user free trial expiration date *******************************************************************************************
    user_free_trial_expiration_date = datetime.strptime(user_telegram_verification_date, date_format) + timedelta(days=get_number_of_free_trial_days())
    # ***************************************************************************************************************************

    # user subscription test ****************************************************************************************************
    # user subscription check using dates ...  current date <= comparison date for subscription validity, > for it to be invalid
    if (
        (user_subscription_expiration_date != '' and current_datetime <= user_subscription_expiration_date) or
        current_datetime <= str(user_free_trial_expiration_date)
    ):
        subscription_valid = True
    else:
        subscription_valid = False
    # ***************************************************************************************************************************

    # subscription expiry date ... pick the most recent date between user_subscription_expiration_date and user_free_trial_expiration_date
    # actual subscription expiry date *********************************************************************************
    if user_subscription_expiration_date > str(user_free_trial_expiration_date):  # most recent date was the actual subscription's expiration date
        subcription_expiry_date = user_subscription_expiration_date
        # set on free trial variable to false ***************************************************************
        on_free_trial = False
        # ***************************************************************************************************
    # *****************************************************************************************************************
    # free trial expiry date ******************************************************************************************
    else: # most recent date was the free trial's expiration date
        subcription_expiry_date = str(user_free_trial_expiration_date)
        # set on free trial variable to false ***************************************************************
        on_free_trial = True
        # ***************************************************************************************************
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # days left till expiration ... return -1 if subscription is nolonger valid *************************************************
    # subcription is no longer valid **********************************************************************************
    if subscription_valid == False: days_till_expiry = -1
    # *****************************************************************************************************************
    # subscription is still valid *************************************************************************************
    else: 
        # date difference
        date_difference = datetime.strptime(subcription_expiry_date, date_format) - datetime.strptime(current_datetime, date_format)
        # number of days left till expiry
        days_till_expiry = date_difference.days
    # *****************************************************************************************************************
    # ***************************************************************************************************************************

    # return subscription status and info
    return subscription_valid, subcription_expiry_date, on_free_trial, days_till_expiry
# *****************************************************************************************************************************************