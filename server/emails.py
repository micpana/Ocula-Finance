from settings import frontend_client_url

# get frontend url
frontend_url = frontend_client_url()

# function for actually sending crafted email
def send_crafted_email(user_email, email_html, email_text):

# email confirmations on registration
def send_registration_email_confirmation(user_email, username, verification_token, token_expiration_date):

# email confirmations on password recovery
def send_password_recovery_email(user_email, username, recovery_token, token_expiration_date):

# email confirmation on email change request
def send_email_change_confirmation(user_email, username, verification_token, token_expiration_date):