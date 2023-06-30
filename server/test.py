from datetime import datetime

date_format = '%Y-%m-%d %H:%M:%S.%f'
date_1 = '2023-12-13 14:32:55.45654'
date_2 = '2023-12-13 14:35:55.45654'

difference = datetime.strptime(date_2, date_format) - datetime.strptime(date_1, date_format)
print(difference)
print(difference.total_seconds())
print(difference.total_seconds() / 60)

if datetime.strptime(date_2, date_format) > datetime.strptime(date_1, date_format):
  print('yeaaaah!')