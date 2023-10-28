def getText(username):
    text = """
yes {username}
now now

nice
    """.format(username = 'micpana', lastname = 'Mudimbu')
    print(username)
    return text

txt = getText('james')
print(txt)
txt = txt.replace('\n', '<br/>')
print(txt)