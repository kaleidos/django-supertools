import pytz
from django.utils import timezone


class TimezoneMiddleware(object):
    def process_request(self, request):
        tzname = request.session.get("timezone", None)
        if tzname:
            timezone.activate(pytz.timezone(tzname))
        else:
            timezone.deactivate()
