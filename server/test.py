# timezone conversion, bard solution ************************************
from pytz import timezone
from datetime import datetime, timedelta, date
from settings import system_timezone

utc_datetime = datetime.now(timezone('UTC'))
est_datetime = utc_datetime.astimezone(timezone(system_timezone()))

print(utc_datetime)
print(est_datetime)

est_str = str(est_datetime)
print(est_str)

# date format
date_format = '%Y-%m-%d %H:%M:%S.%f%z'

new = datetime.strptime(est_str, date_format) + timedelta(days=2)
print(new)

current_day = date.today().isoweekday()

print(current_day)