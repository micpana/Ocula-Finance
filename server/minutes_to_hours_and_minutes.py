# function to convert minutes(float) to hour(s) and minute(s) eg 90 minutes to 1 hour 30 minutes(string) / 30 minutes to just 30 minutes(string)
def minutes_to_hours_and_minutes(minutes_):
    hours = str(minutes_ / 60).split('.')[0]
    hours_append = 'trading hour' if hours == '1' else 'hours'
    hours_text = hours + ' ' + hours_append
    minutes = str(minutes_ % 60)
    minutes_append = 'trading minute' if minutes == '1' else 'minutes'
    minutes_text = minutes + ' ' + minutes_append

    if hours == '0' and minutes != '0':
        hours_and_minutes_string = minutes_text
    elif hours != '0' and minutes == '0':
        hours_and_minutes_string = hours_text
    elif hours != '0' and minutes != '0':
        hours_and_minutes_string = hours_text + ' ' + minutes_text
    elif hours == '0' and minutes == '0':
        hours_and_minutes_string = minutes_text

    return hours_and_minutes_string