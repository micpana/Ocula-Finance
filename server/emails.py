from settings import platform_name, frontend_client_url, sending_emails_via
from zoho_smtp import zoho_smtp_send_email
from gmail_test_smtp import gmail_test_smtp_send_email

# get platform name
platform_brand_name = platform_name()

# get frontend url
frontend_url = frontend_client_url()

# get user's link to follow *****************************************************************************************************
def get_link_to_follow(purpose, token): # purpose: verification / password recovery / signin / contact us
    link = ''
    if purpose == 'verification': link = frontend_url + '/verify-email/' + token
    if purpose == 'password recovery': link = frontend_url + '/new-password-on-recovery/' + token
    if purpose == 'signin': link = frontend_url + '/signin'
    if purpose == 'contact us': link = frontend_url + '/contact-us'

    return link
# *******************************************************************************************************************************

# function for actually sending crafted email ***********************************************************************************
def send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text):
    # send email
    send_via = sending_emails_via()
    if send_via == 'zoho mail':
        zoho_smtp_send_email(user_email, firstname, subject, email_content_html, email_content_text)
    elif send_via == 'gmail test smtp':
        gmail_test_smtp_send_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************
            
# email confirmations on registration *******************************************************************************************
def send_registration_email_confirmation(user_email, username, firstname, lastname, verification_token, token_expiration_date):
    # email subject
    subject = platform_brand_name + ' Email Verification'

    # email html content
    email_content_html = """
Hi {firstname}, <br/><br/>
Thank you for registering with us. Use the following link to verify your email address. <br/>
<a href='{link}'>{link}</a> (Link expires: {token_expiration_date}). <br/>
If you did not signup on {platform_brand_name} please ignore this message. <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('verification', verification_token), user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)
    
    # email text content
    email_content_text = """
Hi {firstname},

Thank you for registering with us. Use the following link to verify your email address.
{link} (Link expires: {token_expiration_date}).
If you did not signup on {platform_brand_name} please ignore this message.

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('verification', verification_token), user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************

# email confirmations on password recovery **************************************************************************************
def send_password_recovery_email(user_email, username, firstname, lastname, recovery_token, token_expiration_date):
    # email subject
    subject = platform_brand_name + ' Password Recovery'

    # email content html
    email_content_html = """
Hi {firstname}, <br/><br/>
You recently requested a password reset, use the following link to reset your password. <br/>
<a href='{link}'>{link}</a> (Link expires: {token_expiration_date}). <br/>
If you did not request a password reset please ignore this message. <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('password recovery', recovery_token), user_email = user_email, username = username, firstname = firstname, lastname = lastname, recovery_token = recovery_token, token_expiration_date = token_expiration_date)
    
    # email content text
    email_content_text = """
Hi {firstname},

You recently requested a password reset, use the following link to reset your password.
{link} (Link expires: {token_expiration_date}).
If you did not request a password reset please ignore this message.

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('password recovery', recovery_token), user_email = user_email, username = username, firstname = firstname, lastname = lastname, recovery_token = recovery_token, token_expiration_date = token_expiration_date)

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************

# email confirmation on email change request ************************************************************************************
def send_email_change_confirmation(user_email, username, firstname, lastname, verification_token, token_expiration_date):
    # email subject
    subject = platform_brand_name + ' Email Change Confirmation'

    # email content html
    email_content_html = """
Hi {firstname}, <br/><br/>
You recently requested an email change, use the following link to verify your new email address. <br/>
<a href='{link}'>{link}</a> (Link expires: {token_expiration_date}). <br/>
If you did not request an email change please ignore this message. <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('verification', verification_token), user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)

    # email content text
    email_content_text = """
Hi {firstname},

You recently requested an email change, use the following link to verify your new email address.
{link} (Link expires: {token_expiration_date}).
If you did not request an email change please ignore this message.

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('verification', verification_token), user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************

# login on new device email notification ****************************************************************************************
def send_login_on_new_device_email_notification(user_email, username, firstname, lastname, date_and_time, user_os, user_device, user_ip_address, user_browser):
    # email subject
    subject = platform_brand_name + ' New Device Login'

    # email content html
    email_content_html = """
Hi {firstname}, <br/><br/>
We detected a login into your account from a new device on {date_and_time}. <br/>
Device used: {user_device}, {user_browser}, {user_os}. <br/>
IP address: {user_ip_address}. <br/>
If it wasn't you, please consider setting a new account password via the Settings tab inside your user dashboard, 
this will also log out all devices currently logged into your account. <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('contact us', None), user_email = user_email, username = username, firstname = firstname, lastname = lastname, date_and_time = date_and_time, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)
    
    # email content text
    email_content_text = """
Hi {firstname},

We detected a login into your account from a new device on {date_and_time}.
Device used: {user_device}, {user_browser}, {user_os}.
IP address: {user_ip_address}.
If it wasn't you, please consider setting a new account password via the Settings tab inside your user dashboard, this will also log out all devices currently logged into your account.

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('contact us', None), user_email = user_email, username = username, firstname = firstname, lastname = lastname, date_and_time = date_and_time, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************

# account email change email notification ***************************************************************************************
def send_account_email_change_email_notification(user_email, username, firstname, lastname, user_os, user_device, user_ip_address, user_browser):
    # email subject
    subject = platform_brand_name + ' Email Change Notification'

    # email content html
    email_content_html = """
Hi {firstname}, <br/><br/>
Your account's new email address has been verified successfully, use the following link to access your account. <br/>
<a href='{link}'>{link}</a>. <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('signin', None), user_email = user_email, username = username, firstname = firstname, lastname = lastname, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)
    
    # email content text
    email_content_text = """
Hi {firstname},

Your account's new email address has been verified successfully, use the following link to access your account.
{link}

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, link = get_link_to_follow('signin', None), user_email = user_email, username = username, firstname = firstname, lastname = lastname, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************

# account role change email notification ****************************************************************************************
def send_account_role_change_email_notification(user_email, username, firstname, lastname, old_role, new_role): # roles = user / admin / free user
    # email subject ***************************************************************************************************
    subject = platform_brand_name + ' Account Access Change Notification'
    # *****************************************************************************************************************

    # notification text ***********************************************************************************************
    if old_role == 'admin' and new_role == 'user':
        notification_text = "Your account's access level has been downgraded. You now have ordinary user level access only."
    elif old_role == 'admin' and new_role == 'free user':
        notification_text = "Your account's access level has been downgraded. You now have ordinary user level access only. However, you have been given free access until further notice. We hope you enjoy your free access period and find it valuable. Happy trading."
    elif (old_role == 'user' or old_role == 'free user') and new_role == 'admin':
        notification_text = 'Your account now has admin access.'
    elif old_role == 'free user' and new_role == 'user':
        notification_text = 'Your account no longer has free access. We really hope you enjoyed your free access period and found it valuable.'
    elif old_role == 'user' and new_role == 'free user':
        notification_text = 'Your account has been given free access until further notice. We hope you enjoy your free access period and find it valuable. Happy trading.'
    # *****************************************************************************************************************

    # email content html **********************************************************************************************
    email_content_html = """
Hi {firstname}, <br/><br/>
{notification_text} <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************
    
    # email content text **********************************************************************************************
    email_content_text = """
Hi {firstname},

{notification_text}

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************

# payment confirmation email ****************************************************************************************************
def send_payment_confirmation_email(user_email, username, firstname, lastname, amount, subcription, subscription_package):
    # email subject ***************************************************************************************************
    subject = platform_brand_name + ' Payment Confirmation'
    # *****************************************************************************************************************

    # notification text ***********************************************************************************************
    if subcription == True:
        notification_text = f'Your payment of ${amount} for our {subscription_package} was successful. Thank you for your continued support.' 
    else:
        notification_text = f'Your payment of ${amount} was successful. Thank you for your continued support.'
    # *****************************************************************************************************************

    # email content html **********************************************************************************************
    email_content_html = """
Hi {firstname}, <br/><br/>
{notification_text} <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # email content text **********************************************************************************************
    email_content_text = """
Hi {firstname},

{notification_text}

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************

# subscription expiration notification email ************************************************************************************
def send_subscription_expiration_notification_email(user_email, username, firstname, lastname, free_trial, expired, days_till_expiry):
    # email subject ***************************************************************************************************
    subject = platform_brand_name + ' Subscription Expiration'
    # *****************************************************************************************************************

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

    # email content html **********************************************************************************************
    email_content_html = """
Hi {firstname}, <br/><br/>
{notification_text} <br/><br/>
Regards, <br/><br/>
{platform_brand_name} Team <br/><br/>
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # email content text **********************************************************************************************
    email_content_text = """
Hi {firstname},

{notification_text}

Regards,

{platform_brand_name} Team
    """.format(platform_brand_name = platform_brand_name, firstname = firstname, notification_text = notification_text)
    # *****************************************************************************************************************

    # send crafted email
    send_crafted_email(user_email, firstname, subject, email_content_html, email_content_text)
# *******************************************************************************************************************************