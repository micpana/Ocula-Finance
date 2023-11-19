code_string = """
# get items
def get_items(a, b, c):
    together = a + ' ' + b + ' ' + c

    gh = 'yes'

    nh = 'no'

    return together, gh, nh
"""

exec(code_string)

print(get_items('now', 'yes', 'sir'))