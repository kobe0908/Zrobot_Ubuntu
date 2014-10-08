#!/usr/bin/env python

from datetime import (
    datetime,
    timedelta
    )


def week_start(dt=None):
    """
    Calculates the ISO week start datetime for the given time
    @param dt: Datetime to calculate from (defaults to now)
    @returns: datetime of week start
    """
    if dt is None:
        dt = datetime.today()
    week_days = datetime.isoweekday(dt) % 7
    week_start = dt - timedelta(days=week_days)
    return week_start.replace(hour=0, minute=0, second=0, microsecond=0)

def utc_date_to_local_datetime(dt):
    if dt is None:
        return None
    utc_offset = datetime.utcnow() - datetime.now()
    return datetime.strptime(dt, "%Y%m%dT%H%M%SZ") - utc_offset

def utc_date_to_isocalendar(timestamp):
    """Converts '20120216T025651Z' into (year, week, weekday) tuple"""
    if timestamp is None:
        return None
    elif type(timestamp) is tuple:
        # Assume already in tuple form, just pass-thru
        return timestamp
    dt = utc_date_to_local_datetime(timestamp)
    if dt is None:
        return None
    return dt.isocalendar()

def total_seconds(td):
    tsec = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6)/10**6
    return tsec

if __name__ == '__main__':
    print week_start()

    td = timedelta(days=10, seconds=2.999)
    dt = datetime.today() - td
    print week_start(dt)

    print "%d == %d\n" %(total_seconds(td), td.total_seconds())
