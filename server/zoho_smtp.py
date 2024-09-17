import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import platform_name

# credentials
email = os.environ.get('ZOHO_SMTP_EMAIL')
password = os.environ.get('ZOHO_SMTP_PASSWORD')

# function for sending emails ***************************************************************************************************
def zoho_smtp_send_email(user_email, firstname, subject, email_content_html, email_content_text):
    # zoho mail login
    server = smtplib.SMTP('smtppro.zoho.com', port=587) # port: 465 with SSL or port: 587 with TLS
    server.ehlo('oculafinance.com')
    server.starttls()
    server.login(email, password)

    # construct email
    message = MIMEMultipart()
    message["To"] = user_email
    message["From"] = email
    message["Subject"] = subject
    title = '<b> {platform_brand_name} </b>'.format(platform_brand_name = platform_name())
    messageText = MIMEText(email_content_html, 'html')
    message.attach(messageText)

    # addresses
    fromaddr = email
    toaddrs  = user_email

    # send email
    server.sendmail(fromaddr, toaddrs, message.as_string())

    server.quit()
# *******************************************************************************************************************************