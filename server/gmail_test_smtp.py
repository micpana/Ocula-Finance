import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from settings import platform_name

# credentials
email = os.environ.get('GMAIL_TEST_SMTP_EMAIL')
password = os.environ.get('GMAIL_TEST_SMTP_PASSWORD')

# function for sending emails ***************************************************************************************************
def gmail_test_smtp_send_email(user_email, firstname, subject, email_content_html, email_content_text):
    # gmail login
    server = smtplib.SMTP('smtp.gmail.com', port=587)
    server.ehlo('Gmail')
    server.starttls()
    server.login(email, password)

    # construct email
    message = MIMEMultipart()
    message["To"] = user_email
    message["From"] = formataddr((platform_name(), email))  # display brand name and email
    message["Subject"] = '(Test Email) ' + subject
    messageText = MIMEText(email_content_html, 'html')
    message.attach(messageText)

    # addresses
    fromaddr = email
    toaddrs  = user_email

    # send email
    server.sendmail(fromaddr, toaddrs, message.as_string())

    server.quit()
# *******************************************************************************************************************************