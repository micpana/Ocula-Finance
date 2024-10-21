from datetime import datetime
from settings import system_timezone
from pytz import timezone

date_format = '%Y-%m-%d %H:%M'
current_datetime = datetime.now(timezone(system_timezone())).strftime(date_format)
current_datetime_object = datetime.strptime(current_datetime, date_format)

print(current_datetime)
print(current_datetime_object)