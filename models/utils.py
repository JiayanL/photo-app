from datetime import datetime

def get_display_time(timestamp):
    diff = datetime.utcnow() - timestamp
    days = diff.days
    seconds = diff.seconds
    hours = seconds // 3600

    # print(diff, days, seconds, hours)
    if days == 0:
        if hours < 1:
            return 'Just now'
        elif hours == 1:
            return '1 hour ago'
        else:
            return '{0} hours ago'.format(hours)
    elif days == 1:
        return '1 day ago'
    else:
        return '{0} days ago'.format(days)