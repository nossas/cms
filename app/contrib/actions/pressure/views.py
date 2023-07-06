import json

from django.http import HttpResponse
from django.views.generic import FormView

from .forms import PressureAjaxForm


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs["content_type"] = "application/json"
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors)  # , status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                "success": True,
            }
            return self.render_to_json_response(data)
        else:
            return response


class PressureFormAjaxView(AjaxableResponseMixin, FormView):
    form_class = PressureAjaxForm
    http_method_names = ["post"]  # Not interested in any GETs here...
    template_name = "pressure/pressure_plugin.html"

    #
    # NOTE: Even though this will never be used, the FormView requires that
    # either the success_url property or the get_success_url() method is
    # defined. So, let use the sensible thing and set it to the page where
    # this plugin is coming from.
    #
    def get_success_url(self):
        return self.request.path

    def form_valid(self, form):
        # AjaxableResponseMixin expects our contact object to be 'self.object'.
        self.object = form.submit()
        return super(PressureFormAjaxView, self).form_valid(form)
