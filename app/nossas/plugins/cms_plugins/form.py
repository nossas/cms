from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from djangocms_forms.cms_plugins import FormPlugin as DjangoCMSFormPlugin


plugin_pool.unregister_plugin(DjangoCMSFormPlugin)


@plugin_pool.register_plugin
class FormPlugin(DjangoCMSFormPlugin):
    fieldsets = (
        (
            _("Configurações"),
            {
                "fields": (
                    ("name", "submit_btn_txt"),
                    "form_template",
                    "post_submit_msg",
                ),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        return self.fieldsets
