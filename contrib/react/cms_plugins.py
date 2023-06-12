from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import Email
from .forms import EmailForm

@plugin_pool.register_plugin
class ReactPlugin(CMSPluginBase):
    name = "ReactPlugin"
    render_template = "react/plugins/react.html"
    # model = Email
    # form = EmailForm
    change_form_template = "react/admin/change_form.html"

    # def get_form(self, request, obj, change=False, **kwargs):
    #     return EmailForm
    #     # return super().get_form(request, obj, change, **kwargs)
    
    # def save_form(self, request, form, change):
    #     form = super(ReactPlugin, self).save_form(request, form, change)

    #     return form