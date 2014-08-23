from django.core.urlresolvers import reverse
from django.views.generic import View
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response

from .. import http
from .. import exceptions as exc


class GenericView(View):
    response_cls = http.HttpResponse
    content_type = "text/html"
    permissions = ()

    def handle_exception(self, exception):
        """
        Ad-hoc exception handling for all derived views.
        """
        ctx = {"exception": exception}

        if isinstance(exception, exc.RedirectRequired):
            return self.redirect(url=exception.detail)
        elif isinstance(exception, exc.IntegrityError):
            return http.HttpConflict(exception)

        return exception

    def init(self, request, *args, **kwargs):
        pass

    def get_context_data(self):
        context = {"view": self}
        context.update(self.kwargs)
        return context

    def __handle_permissions(self):
        for fn in self.permissions:
            result = fn(self)
            if isinstance(result, http.HttpResponse):
                return result
            elif result == False:
                raise exc.PermissionDenied("Forbidden")

        if hasattr(self, "handle_permissions"):
            return self.handle_permissions()

    def dispatch(self, request, *args, **kwargs):
        try:
            self.init(request, *args, **kwargs)
            result = self.__handle_permissions()
            if isinstance(result, http.HttpResponse):
                return result
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            response = self.handle_exception(e)
            if isinstance(response, Exception):
                raise
            return response

    def redirect(self, reverseurl=None, *, url=None, args=None, kwargs=None):
        """
        Simple redirect helper.
        """
        if not url:
            url = reverse(reverseurl, args=args, kwargs=kwargs)
        return http.HttpRedirect(url)

    def render(self, template=None, context=None, data=None,
               response_cls=None, content_type=None, status_code=None):

        output_data = data or b""

        if template:
            _context = self.get_context_data()
            _context.update(context or {})

            context_instance = RequestContext(self.request)
            output_data = render_to_string(template, _context,
                                           context_instance=context_instance)

        if content_type is None:
            content_type = self.content_type

        if not response_cls:
            response_cls = self.response_cls

        response = response_cls(output_data, content_type=content_type)
        if status_code:
            response.status_code = status_code

        return response


class GenericTemplateView(GenericView):
    tmpl_name = None

    def get(self, request, *args, **kwargs):
        if self.tmpl_name is None:
            raise ValueError("tmpl_name attr must be a valid template name")
        return self.render(self.tmpl_name)
