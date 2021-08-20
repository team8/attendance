import calendar
from datetime import datetime, timedelta, date


def convert_time(time):
    timestamp = calendar.timegm(time.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert time.resolution >= timedelta(microseconds=1)
    real_hours = local_dt.replace(microsecond=time.microsecond)
    return real_hours
