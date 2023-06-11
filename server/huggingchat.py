import joblib
from hugchat import hugchat
from hugchat.login import Login
from settings import get_cookies_path, get_error_logs_path

# log in to huggingface and grant authorization to huggingchat
hc_email = "michaelmudimbu@gmail.com"
hc_password = "Imika@2023"

# check if we have cookies from a saved session, if so, use those cookies, if not, login and save cookies
cookies_path = get_cookies_path('HuggingChat-Cookies') # input = name string
try:
    cookies = joblib.load(cookies_path)
    print('HuggingChat session found, using existing cookies')
except: # no saved cookies, login
    print('No HuggingChat session found, login in and saving cookies')
    sign = Login(hc_email, hc_password)
    cookies = sign.login()
    # save cookies
    joblib.dump(cookies, cookies_path)

# create a ChatBot
print('Connecting to HuggingChat ...')
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
print('Connection successful.')

# query huggingchat ai
def query_huggingchat_ai(prompt, new_conversation, conversation_list):
    if new_conversation == True:
        # Create a new conversation
        id = chatbot.new_conversation()
        chatbot.change_conversation(id)

    if conversation_list == True:
        # Get conversation list
        conversation_list = chatbot.get_conversation_list()
        print(conversation_list)

    # get response
    while True:
        try:
            print('Querying HuggingChat ...')
            response = chatbot.chat(prompt)
            print('Successful.')
            break
        except Exception as e:
            print(e)
            print('Error encountered while querying HuggingChat. Retrying ...')

    return response

# for testing *************************************************
# user_input = None
# while True:
#     if user_input != 'quit':
#         if user_input == None:
#             user_input = input('Enter prompt: ')
#         else:
#             print(query_huggingchat_ai(user_input, False, True))
#             user_input = None
#     else:
#         break