import re
def is_password_structure_valid(password):
	if len(password) < 8: # password length
		return False
	if not re.search(r"[!@#$%^&*(),.?\":{}|<>/'`~]", password): # special characters
		return False
	if not re.search(r'[A-Z]', password): # uppercase letters
		return False
	if not re.search(r'[a-z]', password): # lowercase letters
		return False
	if not re.search(r'\d', password): # numbers
		return False
	# if all conditions are met, password is valid
	return True

print(is_password_structure_valid('#l.jM1/`,'))