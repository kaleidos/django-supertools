from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from .. import exceptions as exc


PAGINATOR_NUMBERS_AFTER_CURRENT = 3
PAGINATOR_NUMBERS_BEFORE_CURRENT = 3
PAGINATOR_NUMBERS_AT_BEGIN = 2
PAGINATOR_NUMBERS_AT_END = 1


class PaginatorMixin(object):
    page_param = "page"
    page_size = 30

    def paginate(self, queryset, page_param='page', page_size=None, raise_when_overflow=False):
        """
        Updates context with a member called 'page'. This member contains the queryset paginated.

        :param QuerySet queryset: objects queryset to paginate
        :param dict context: base context to update
        :param str page_param: request get param used for page number
        :return: context updated with pagination info
        :rtype: dict
        """
        if page_size is None:
            page_size = self.page_size

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
