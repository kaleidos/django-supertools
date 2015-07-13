# -*- coding: utf-8 -*-
"""Serializers are used to transform between different media types.

They are mainly used in the HTTP cycle to handle various media-type representation of the same
data, for example, as json, html and others.
"""

from __future__ import absolute_import

import json

from django.conf import settings
from django.template.loader import get_template
from django.utils import six
from django.utils.datastructures import MergeDict
from django.utils.functional import cached_property

from .json import LazyEncoder


def get_request_encoding(request):
    return getattr(request, "encoding", None) or settings.DEFAULT_CHARSET


class SerializersContainer(object):
    """
    Wrapper around a collection of serializers that supports additional operations.
    """

    __slots__ = ("serializers", "default_serializer")

    def __init__(self, default_serializer, *serializers):
        self.default_serializer = default_serializer
        self.serializers = (default_serializer,) + serializers

    def accept_content_type(self, content_type):
        return bool(self.get_by_content_type(content_type))

    def get_by_content_type(self, content_type):
        for serializer in self.serializers:
            if serializer.accepts_content_type(content_type):
                return serializer
        return None

    def get_default(self) :
        return self.default_serializer

    def get_default_content_type(self):
        return self.get_default().content_type

    def __len__(self):
        return len(self.serializers)

    def __add__(self, serializer):
        serializers = self.serializers + (serializer,)
        return type(self)(serializers[0], *serializers[1:])

    def __iter__(self):
        return iter(self.serializers)


class Serializer(object):
    """Abstract serializer.

    Defines a common api for concrete serializers.
    Each serializer is bound to a content type and can be queried for its support.
    """
    content_type = None

    def loads(self, data=None, request=None):
        raise NotImplementedError

    def dumps(self, data, request=None, response=None):
        raise NotImplementedError

    def accepts_content_type(self, content_type):
        raise NotImplementedError


class Json(Serializer):
    """Transform between json-encoded text and python built-in data types."""
    content_type = "application/json"

    def loads(self, request, data=None):
        if data is None:
            data = request.body

        if not data:
            return None

        if not isinstance(data, six.binary_type):
            data = data.decode(get_request_encoding(request))

        return json.loads(data)

    def dumps(self, data, request=None, response=None):
        return json.dumps(data, cls=LazyEncoder, ensure_ascii=False).encode(
            get_request_encoding(request))

    def accepts_content_type(self, content_type):
        return self.content_type in content_type or "+json" in content_type


class MultiPart(Serializer):
    """Allow multipart requests. This serializer only serves for request decoding."""
    content_type = "multipart/form-data"

    def loads(self, request, data=None):
        return MergeDict(request.POST, request.FILES)

    def accepts_content_type(self, content_type):
        return self.content_type in content_type


class PrettyJson(Json):

    def dumps(self, data, request=None, response=None):
        return json.dumps(data, cls=LazyEncoder, indent=4, sort_keys=True)


class HtmlJson(Serializer):
    """Transform between html-encoded json text and python built-in data types."""

    content_type = "text/html"
    template_name = "http/api.html"

    def __init__(self, template_name=None):
        if template_name:
            self.template_name = template_name
        self.json = PrettyJson()

    @cached_property
    def template(self):
        return get_template(self.template_name)

    def dumps(self, data, request=None, response=None):
        return self.template.render({
            "data": self.json.dumps(data, request, response),
            "request": request,
            "response": response
        })

    def accepts_content_type(self, content_type):
        return self.content_type in content_type
