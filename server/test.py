def getTex(username):
    text = """
yes {username}
now now

nice
    """.format(username = 'micpana', lastname = 'Mudimbu')
    print(username)
    return text

getText = getTex
print(getText)
txt = getText('james')
print(txt)
txt = txt.replace('\n', '<br/>')
print(txt)