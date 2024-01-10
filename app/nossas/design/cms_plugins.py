from cms.plugin_base import CMSPluginBase


class UICMSPluginBase(CMSPluginBase):
    change_form_template = "design/admin/ui_cms_plugin_change_form.html"
    # custom_fieldsets = {}


# class UIPaddingMixin:
#     blockname = "Espaçamento"
#     blockfields = ("padding_x", "padding_y")

#     def __init__(self, *args, **kwargs):
#         self.custom_fieldsets.update({self.blockname: self.blockfields})

#         super().__init__(*args, **kwargs)


# class UIBackgroundMixin:
#     blockname = "Fundo"
#     blockfields = [
#         "background",
#     ]

#     def __init__(self, *args, **kwargs):
#         self.custom_fieldsets.update({self.blockname: self.blockfields})

#         super().__init__(*args, **kwargs)


# class UIBorderMixin:
#     blockname = "Borda"
#     blockfields = [
#         "border_start",
#         "border_end",
#         "border_top",
#         "border_bottom",
#     ]

#     def __init__(self, *args, **kwargs):
#         self.custom_fieldsets.update({self.blockname: self.blockfields})

#         super().__init__(*args, **kwargs)
