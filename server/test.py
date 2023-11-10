from datetime import datetime
date = str(datetime.now())

print(date)

date = date.replace('-', '').replace(':', '').replace('.', '').replace(' ', '')[::-1]

print(date)

print(len(date))