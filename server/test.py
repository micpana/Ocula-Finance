from datetime import datetime

start_date = '2023-11-22 00:11'
try: datetime.strptime(start_date, '%Y-%m-%d'); print('good')
except: print('bad')