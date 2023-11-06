from datetime import datetime, timedelta

subscription_months = 1

current_datetime_object = datetime.now()
expiry_date = str(current_datetime_object + timedelta(weeks = (subscription_months * 4)))

print(expiry_date)