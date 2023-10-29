text = 'a b c'

ls = [['a','A'], ['b','B'], ['c','C']]

new = text
for item in ls:
    tag = item[0]
    replacement = item[1]

    new = new.replace(tag, replacement)

print(new)