from .. import exceptions as exc

class FormViewMixin(object):
    # Simple heleprs for dealing with forms

    def get_form_cls(self):
        if not hasattr(self, "form_cls"):
            raise exc.InternalError("form_cls attribute not defined")
        return self.form_cls

    def get_form(self, initial=None, **kwargs):
        form_cls = self.get_form_cls()
        if self.request.method == "POST":
            return form_cls(self.request.POST, self.request.FILES, initial=initial, **kwargs)
        return form_cls(initial=initial, **kwargs)
