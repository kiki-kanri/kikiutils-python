import datetime as _datetime
import time as _time


# Time

def get_time_zone_offset(get_type: str = 's'):
    """Get time zone offset. Default return seconds."""

    zone_offset = _time.timezone if (_time.localtime().tm_isdst == 0) else _time.altzone

    if get_type == 'h':
        return round(zone_offset / 3600)
    else:
        return zone_offset


def int_time(time_str: str, format_str: str = '%Y-%m-%d %a %H:%M:%S', use_zone: bool = False):
    """Convert string datetime to timestamp."""

    struct_time = _time.strptime(time_str, format_str)
    timestamp = int(_time.mktime(struct_time))

    if use_zone:
        return timestamp + get_time_zone_offset()
    else:
        return timestamp


def now_time(get_timestamp: bool = False, str_format: str = '%Y-%m-%d %a %H:%M:%S'):
    """Get now time."""

    now = _datetime.datetime.now()
    return int(_time.mktime(now.timetuple())) if get_timestamp else str(now.strftime(str_format))


def now_time_ms():
    """Get now timestamp(ms)."""

    return round(_time.time() * 1000)


def now_time_utc():
    """Get now utc timestamp."""

    zone_offset = get_time_zone_offset()
    return now_time(True) + zone_offset


def now_time_utc_ms():
    """Get now utc timestamp(ms)."""

    zone_offset = get_time_zone_offset()
    return now_time_ms() + (zone_offset * 1000)


def str_time(timestamp: int, str_format: str = '%Y-%m-%d %a %H:%M:%S', use_zone: bool = False):
    """Change timestamp to str time."""

    if use_zone:
        timestamp -= get_time_zone_offset()

    datetime = _datetime.datetime.fromtimestamp(timestamp)
    return datetime.strftime(str_format)
