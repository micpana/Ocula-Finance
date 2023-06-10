from hugchat import hugchat
from hugchat.login import Login

# log in to huggingface and grant authorization to huggingchat
hc_email = "michaelmudimbu@gmail.com"
hc_password = "Imika@2023"
sign = Login(hc_email, hc_password)
cookies = sign.login()

# save cookies to usercookies/<email>.json
sign.saveCookies()

# create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())  # or cookie_path="usercookies/<email>.json"

# query huggingchat ai
def query_huggingchat_ai(prompt):
    # get response
    response = chatbot.chat(prompt)

    return response