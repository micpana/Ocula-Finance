import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from settings import platform_name

# credectials
email = os.environ.get('GMAIL_TEST_SMTP_EMAIL')
password = os.environ.get('GMAIL_TEST_SMTP_PASSWORD')

# function for sending emails
def gmail_test_smtp_send_email(user_email, firstname, subject, email_content_html, email_content_text):

    message = MIMEMultipart()
    message["To"] = user_email
    message["From"] = email
    message["Subject"] = '(Test Email) ' + subject

    title = '<b> {platform_brand_name} </b>'.format(platform_brand_name = platform_name())
    messageText = MIMEText(email_content_html, 'html')
    message.attach(messageText)

    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo('Gmail')
    server.starttls()
    server.login(email,password)
    fromaddr = email
    toaddrs  = user_email
    server.sendmail(fromaddr,toaddrs,message.as_string())

    server.quit()