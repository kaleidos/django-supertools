from contextlib import contextmanager

from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied as DjangoPermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
from django.http import Http404
from django.db import IntegrityError
from django.shortcuts import resolve_url


from . import http


class BaseException(Exception):
    default_content = _("Unexpected error")
    response_class = http.BadRequest

    def __init__(self, detail=None):
        self.content = detail or self.default_content


class UnsupportedMediaType(BaseException):
    response_class = http.UnsupportedMediaType


class MethodNotAllowed(BaseException):
    response_class = http.MethodNotAllowed


class NotAcceptable(BaseException):
    response_class = http.NotAcceptable


class NotFound(BaseException, Http404):
    default_content = _("Not found.")
    response_class = http.NotFound


class Forbidden(BaseException, DjangoPermissionDenied):
    response_class = http.Forbidden
    default_content = _("Permission denied")


class Unauthorized(BaseException):
    response_class = http.Unauthorized


class BadRequest(BaseException):
    pass


class WrongArguments(BadRequest):
    default_content = _("Wrong arguments.")


class ValidationError(BadRequest):
    default_content = _("Data validation error")


class Redirect(BaseException):
    response_class = http.TemporaryRedirect


class RedirectPermanent(BaseException):
    response_class = http.MovedPermanently


class IntegrityError(BaseException):
    default_content = _("Integrity Error for wrong or invalid arguments")
    response_class = http.Conflict


class InternalError(BaseException):
    default_content = _("Internal server error")
    response_class = http.InternalServerError


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
