# -*- coding: utf-8 -*-

import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.utils.functional import Promise
from django.utils import timezone

# Python3 compatibility
try:
    from django.utils.encoding import force_unicode as force_text
except ImportError:
    from django.utils.encoding import force_text


class LazyEncoder(DjangoJSONEncoder):
    """
    JSON encoder class for encode correctly traduction strings.
    Is for ajax response encode.
    """

    def default(self, obj):
        if isinstance(obj, Promise):
            return force_text(obj)
        elif isinstance(obj, datetime.datetime):
            obj = timezone.localtime(obj)
        return super(LazyEncoder, self).default(obj)


def to_json(data, **kwargs):
    return json.dumps(data, cls=LazyEncoder, **kwargs)
