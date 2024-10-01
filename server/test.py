import string 
import random 

def generate_telegram_connect_code():
    token_length = 6
    token_characters = string.digits
    token = "".join(random.choice(token_characters) for _ in range(token_length))
    return token
print(generate_telegram_connect_code())

