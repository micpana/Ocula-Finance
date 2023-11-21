from mailjet_rest import Client
import os
from settings import platform_name

# credentials
api_key = os.environ.get('MAILJET_API_KEY')
api_secret = os.environ.get('MAILJET_SECRET')

# initiate mailjet client
mailjet = Client(auth=(api_key, api_secret), version='v3.1')

# function for sending emails
def mailjet_send_email(user_email, firstname, subject, email_content_html, email_content_text):
    data = {
        'Messages': [
            {
            "From": {
                "Email": "oculafinance@gmail.com",
                "Name": platform_name()
            },
            "To": [
                {
                "Email": user_email,
                "Name": firstname
                }
            ],
            "Subject": subject,
            "TextPart": email_content_text,
            "HTMLPart": email_content_html,
            "CustomID": "AppGettingStartedTest"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
