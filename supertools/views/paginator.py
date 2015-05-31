from django.conf import settings
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .. import exceptions as exc


PAGINATOR_PAGE_PARAM  = getattr(settings, "PAGINATOR_PAGE_PARAM", "page")
PAGINATOR_PAGE_SIZE  = getattr(settings, "PAGINATOR_PAGE_SIZE", 30)
PAGINATOR_NUMBERS_AFTER_CURRENT = getattr(settings, "PAGINATOR_NUMBERS_AFTER_CURRENT", 3)
PAGINATOR_NUMBERS_BEFORE_CURRENT = getattr(settings, "PAGINATOR_NUMBERS_BEFORE_CURRENT", 3)
PAGINATOR_NUMBERS_AT_BEGIN = getattr(settings, "PAGINATOR_NUMBERS_AT_BEGIN", 2)
PAGINATOR_NUMBERS_AT_END = getattr(settings, "PAGINATOR_NUMBERS_AT_END", 1)


class PaginatorMixin(object):
    page_param = PAGINATOR_PAGE_PARAM
    page_size = PAGINATOR_PAGE_SIZE

    def paginate(self, queryset, page_param=None, page_size=None, raise_when_overflow=False):
        """
        Updates context with a member called 'page'. This member contains the queryset paginated.

        :param QuerySet queryset: objects queryset to paginate.
        :param str page_param: request get param used for page number.
        :param str page_size: number of items per page.
        :param bool raise_when_overflow: if True a HTTP 404 - Not Found error will be raised.
        :return: context updated with pagination info
        :rtype: dict
        """
        if page_size is None:
            page_size = self.page_size

        if page_param is None:
            page_param = self.page_param

        paginator = Paginator(queryset, page_size)
        page_num = self.request.GET.get(page_param) or 1

        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page = paginator.page(paginator.num_pages)
            if raise_when_overflow:
                raise exc.NotFound("page not found")

        paginator.after_current = PAGINATOR_NUMBERS_AFTER_CURRENT
        paginator.before_current = PAGINATOR_NUMBERS_BEFORE_CURRENT
        paginator.at_begin = PAGINATOR_NUMBERS_AT_BEGIN
        paginator.at_end = PAGINATOR_NUMBERS_AT_END
        return page
