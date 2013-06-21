# -*- coding: utf-8 -*-

import datetime
from django.utils import timezone


def datetime_to_ecma262(value):
    """
    Convert a convencional datetime object
    to ecma-262 javascript/json format.
    """
    r = value.isoformat()
    if value.microsecond:
        r = r[:23] + r[26:]
    if r.endswith('+00:00'):
        r = r[:-6] + 'Z'
    return r


def ecma262_to_datetime(value):
    """
    Convert ecma-262 javascript format to
    correct python datetime format.

    This always return a timezone aware datetimes
    with utc as timezone.
    """

    spec = "%Y-%m-%dT%H:%M:%S.%f"
    is_utc = False

    if value.endswith("Z"):
        is_utc = True
        value = value[:-1]

    dt = strptime(value, spec)
    if is_utc:
        return timezone.make_aware(dt, timezone.utc)

    dt = timezone.make_aware(dt, timezone.get_current_timezone())
    dt = timezone.astimezone(timezone.utc)
    dt = timezone.utc.normalize(dt)
    return dt
