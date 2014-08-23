from contextlib import contextmanager

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import resolve_url


class BaseException(Exception):
    default_detail = _("Unexpected error")

    def __init__(self, detail=None):
        self.detail = detail or self.default_detail

    def __str__(self):
        return force_text(self.detail)


class NotFound(BaseException, Http404):
    default_detail = _("Not found.")


class BadRequest(BaseException):
    pass


class WrongArguments(BadRequest):
    default_detail = _("Wrong arguments.")


class ValidationError(BadRequest):
    default_detail = _("Data validation error")


class PermissionDenied(BaseException, DjangoPermissionDenied):
    default_detail = _("Permission denied")


class RedirectRequired(BaseException):
    def __init__(self, *args, **kwargs):
        self.detail = reverse(*args, **kwargs)


class IntegrityError(BaseException, IntegrityError):
    default_detail = _("Integrity Error for wrong or invalid arguments")


class InternalError(BaseException):
    default_detail = _("Internal server error")


@contextmanager
def supress_exceptions(*exceptions):
    """
    Util context manager for avoid empty
    try/except:pass blocks and put them in more
    idiomatic code.
    """
    try:
        yield
    except exceptions as e:
        pass
