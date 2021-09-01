from datetime import datetime


def to_datetime(date, time):
    try:
        return datetime.strptime(f'{date} {time}', '%Y-%m-%d %H:%M')
    except:
        return None
    # return datetime(*[int(v) for v in date.replace('T', '-').replace(':', '-').split('-')])


def to_date(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except:
        return None


def to_int(value):
    try:
        if len(value) > 9:
            return None
        return int(value)
    except:
        return None


def to_float(value):
    try:
        if len(value) > 9:
            return None
        return float(value)
    except:
        return None