ls = [
    {'item': 'this'},
    {'item': 'this'},
    {'item': 'this'},
    {'item': 'this'},
    {'item': 'this'},
    {'item': 'this'}
]

def delete_password(item):
    del item['item']
    yes = 'NOW'
    item['yes'] = yes.lower()
    item['no'] = item['yes'].upper()
    return item

ls = [
    delete_password(i) for i in ls if True
]

print(ls)