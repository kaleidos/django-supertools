# -*- coding: utf-8 -*-

from django.utils.datastructures import MergeDict


class RequestMergeDataMiddleware(object):
    """
    Inject request.DATA attribute containing a merge
    of GET, POST, and FILES attributes.

    Usefull for WTForms due it only accept one
    data parameter instead of two as django forms.
    """

    def process_request(self, request):
        request.DATA = MergeDict(request.GET,
                                 request.POST,
                                 request.FILES)
