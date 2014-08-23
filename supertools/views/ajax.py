from .. import json
from .. import exceptions as exc


class AjaxMixin(object):
    def handle_exception(self, exception):
        """
        Ad-hoc exception handling for all derived views.
        """
        ctx = {"_error": str(exception)}

        if isinstance(exception, exc.WrongArguments):
            return self.render_json(ctx,  status_code=http.HTTP_400_BAD_REQUEST)

        return super().handle_exception(exception)

    def render_json(self, data, *, content_type=None, status_code=None):
        if content_type is None:
            content_type = "application/json"

        return self.render(data=json.to_json(data),
                           content_type=content_type,
                           status_code=status_code)

