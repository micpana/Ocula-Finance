import random
import string

def generate_access_token():
  """Generates a random access token."""
  token_length = 32
  token_characters = string.ascii_lowercase + string.digits + string.ascii_uppercase 
  token = "".join(random.choice(token_characters) for _ in range(token_length))
  return token

if __name__ == "__main__":
  access_token = generate_access_token()
  print(access_token)
