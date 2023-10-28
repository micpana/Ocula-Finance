role = 'admi'
roles = 'admin/support/user'

if role in roles.split('/'):
    print('yes')
else:
    print('no')