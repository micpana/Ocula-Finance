import getpass

code_string = """
# get items
def get_items(a, b, c):
    together = a + ' ' + b + ' ' + c

    gh = 'yes'

    nh = 'no'

    return together, gh, nh

z, k, j = get_items('good', 'evening', 'sir')

print(z, k, j)

"""

passkey = getpass.getpass("Enter Passkey: ")

exec(code_string)