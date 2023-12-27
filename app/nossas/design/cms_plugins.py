from cms.plugin_base import CMSPluginBase

from djangocms_frontend.helpers import insert_fields


class CMSUIPlugin(CMSPluginBase):
    pass


class UIPaddingMixin:
    blockname = "Padding"

    # def get_fieldsets(self, request, obj=None):
    #     return insert_fields(
    #         super().get_fieldsets(request, obj),
    #         (("padding_x", "padding_y"), ),
    #         block=None,
    #         position=-1,
    #         blockname=self.blockname,
    #     )

    # def render(self, context, instance, placeholder):
    #     classes = [
    #         instance.attributes[field]
    #         for field in ("padding_x", "padding_y")
    #         if field in instance.attributes and instance.attributes[field]
    #     ]
    #     instance.add_class(classes)

    #     return super().render(context, instance, placeholder)



class UIBackgroundMixin:
    blockname = "Background"