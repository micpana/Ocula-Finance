from cryptography.fernet import fernet

# generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
print('\n\nKey: \n', key)