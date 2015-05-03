# -*- coding: utf-8 -*-

"""In the Hypertext Transfer Protocol (HTTP), content negotiation is the mechanism that is used,
when facing the ability to serve several equivalent contents for a given URI, to provide the best
suited one to the final user. The determination of the best suited content is made through one of
three mechanisms:

1. Specific HTTP headers by the client (server-driven negotiation)
2. The 300 Multiple Choices or 406 Not Acceptable HTTP response codes by the server (agent-driven
negotiation)
3. Cache (transparent negotiation).

This module implements the agent-driven negotiation.
"""

from __future__ import absolute_import


def parse_media_range(media_range):
    """Parse a media range string.

    :param media_range: Media range string.

    :return: List of `MediaType` instances.
    """
    result = []
    for media_type in media_range.split(","):
        parts = media_type.split(";")
        type_subtype = parts[0].split("/")
        if len(type_subtype) == 1:
            type = subtype = type_subtype
        else:
            type, subtype = type_subtype
        params = dict(p.split("=") for p in parts[1:])
        q = params.pop("q", 1)
        result.append(MediaType(type, subtype, params, q))

    return result


def parse_and_sort_media_range(media_range):
    """Parse a media range string and return the media types sorted.

    :param media_range: Media range string.

    :return: List of `MediaType` instances sorted by user agent's preference.
    """
    return sorted(parse_media_range(media_range), reverse=True)


def intersect_media_types(requested_media_types, supported_media_types):
    """Returns the `MediaType` resulting of the intersection between two sets of media types."""
    for requested_media_type in requested_media_types:
        for media_type in supported_media_types:
            if media_type.accepts(requested_media_type):
                return media_type
    return None


class MediaType(object):
    """Representation of a media type defined in a media range.

    For more information on media ranges see:
    http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html

    :param type: String with the type.
    :param subtype: String with the subtype.
    :param params: Dict of attribute-value pairs.
    :param q: Value of the relative quality factor. Must be between 0 and 1.
    """
    def __init__(self, type="*", subtype="*", params=None, q=1):
        self.type = type.strip()
        self.subtype = subtype.strip()
        if params is None:
            params = {}
        self.params = params
        self.q = float(q)

    def accepts(self, media_type):
        if media_type.type == "*":
            return True

        elif self.type == media_type.type:
            return self.subtype == media_type.subtype or media_type.subtype == "*"

        return False

    def __str__(self):
        text = "{0.type}/{0.subtype}".format(self)
        params = self.params
        params = {"{}={}".format(key, value) for key, value in self.params.items()}
        if params:
            text = "{};{}".format(text, ";".join(params))

        return text

    def __lt__(self, other):
        if self == other:
            return False

        if self.q != other.q:
            return self.q < other.q

        if self.type == "*":
            return other.type != "*"

        if self.subtype == "*":
            return other.subtype != "*"

        return len(self.params) < len(other.params)

    def __gt__(self, other):
        if self == other:
            return False
        return not self < other

    def __eq__(self, other):
        return (self.type == other.type and
                self.subtype == other.subtype and
                self.q == other.q and
                self.params == other.params)
