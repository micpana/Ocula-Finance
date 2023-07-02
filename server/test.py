from datetime import datetime

date_format = '%Y-%m-%d %H:%M'
current_datetime = datetime.now().strftime(date_format)
current_datetime_object = datetime.strptime(current_datetime, date_format)

print(str(current_datetime_object))