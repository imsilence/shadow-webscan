#encoding: utf-8

from datetime import datetime, timedelta

def now():
    return datetime.now()

def datetime_format(dt=None):
    if dt is None:
        dt = now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')
