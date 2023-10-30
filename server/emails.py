from settings import frontend_client_url

# get frontend url
frontend_url = frontend_client_url()

# function for actually sending crafted email ************************************************************************************
def send_crafted_email(user_email, email_content_html, email_content_text):



# email confirmations on registration ********************************************************************************************
def send_registration_email_confirmation(user_email, username, firstname, lastname, verification_token, token_expiration_date):
    # email html content
    email_content_html = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)
    
    # email text content
    email_content_text = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)

    # send crafted email
    send_crafted_email(user_email, email_content_html, email_content_text)

# email confirmations on password recovery ***************************************************************************************
def send_password_recovery_email(user_email, username, firstname, lastname, recovery_token, token_expiration_date):
    # email content html
    email_content_html = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, recovery_token = recovery_token, token_expiration_date = token_expiration_date)
    
    # email content text
    email_content_text = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, recovery_token = recovery_token, token_expiration_date = token_expiration_date)

    # send crafted email
    send_crafted_email(user_email, email_content_html, email_content_text)

# email confirmation on email change request *************************************************************************************
def send_email_change_confirmation(user_email, username, firstname, lastname, verification_token, token_expiration_date):
    # email content html
    email_content_html = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)

    # email content text
    email_content_text = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, verification_token = verification_token, token_expiration_date = token_expiration_date)

    # send crafted email
    send_crafted_email(user_email, email_content_html, email_content_text)

# login on new device email notification *****************************************************************************************
def send_login_on_new_device_email_notification(user_email, username, firstname, lastname, user_os, user_device, user_ip_address, user_browser):
    # email content html
    email_content_html = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)
    
    # email content text
    email_content_text = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)

    # send crafted email
    send_crafted_email(user_email, email_content_html, email_content_text)

# account email change email notification ****************************************************************************************
def send_account_email_change_email_notification(user_email, username, firstname, lastname, user_os, user_device, user_ip_address, user_browser):
    # email content html
    email_content_html = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)
    
    # email content text
    email_content_text = """

    """.format(user_email = user_email, username = username, firstname = firstname, lastname = lastname, user_os = user_os, user_device = user_device, user_ip_address = user_ip_address, user_browser = user_browser)

    # send crafted email
    send_crafted_email(user_email, email_content_html, email_content_text)