from django import forms
from django.db import transaction

from cms.models import Page
from cms.forms.wizards import CreateCMSPageForm
from cms.utils.conf import get_cms_setting

from contrib.bonde.forms import ReferenceBaseModelForm
from contrib.bonde.widgets import ActionSelectWidget, ActionChoices
from contrib.frontend.landpage.layouts import Layout


class WidgetBaseForm(CreateCMSPageForm):
    # Reset inheritance fields
    content = None
    # Settings widget kind
    action_kind = None
    # TODO: Rename this to action_id
    # widget_id = forms.IntegerField(help_text="Insira o ID da Widget criada no Bonde.")

    # class Media:
    #     js = ("//ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js",)

    # class Meta:
    #     model = Page
    #     fields = ("title", "slug", "widget_id")

    def __init__(self, *args, **kwargs):
        super(WidgetBaseForm, self).__init__(*args, **kwargs)

        if not self.action_kind:
            raise NotImplementedError("Should be settings action_kind attribute")

        # Configurar tipo de ação para filtrar widgets
        # self.fields["widget_id"].choices = ActionChoices(self.action_kind)
    
    @transaction.atomic
    def save(self, **kwargs):
        from cms.api import add_plugin

        new_page = super().save(**kwargs)

        slot = "content"
        placeholder = self.get_placeholder(new_page, slot=slot)

        for layout in ["hero", self.action_kind, "four_columns", "signature"]:
            block_plugin = add_plugin(
                placeholder=placeholder,
                plugin_type="BlockPlugin",
                language=self.language_code,
                # layout=self.action_kind,
                # background_color="blue"
                # body=self.color_apply(text_html, element="h1")
                # if self.is_dark()
                # else text_html,
            )

            Layout(obj=block_plugin, layout=layout).copy()
        # if self.cleaned_data.get("page_type"):
        #     return new_page

        # parent_node = self.cleaned_data.get('parent_node')

        # if parent_node and new_page.parent_page.is_page_type:
        #     # the new page was created under a page-type page
        #     # set the new page as a page-type too
        #     new_page.update(
        #         draft_only=True,
        #         is_page_type=True,
        #         in_navigation=False,
        #     )

        # # If the user provided content, then use that instead.
        # content = self.cleaned_data.get('content')
        # plugin_type = get_cms_setting('PAGE_WIZARD_CONTENT_PLUGIN')
        # plugin_body = get_cms_setting('PAGE_WIZARD_CONTENT_PLUGIN_BODY')
        # slot = get_cms_setting('PAGE_WIZARD_CONTENT_PLACEHOLDER')

        # if plugin_type in plugin_pool.plugins and plugin_body:
        #     if content and permissions.has_plugin_permission(
        #             self.user, plugin_type, "add"):
        #         new_page.rescan_placeholders()
        #         placeholder = self.get_placeholder(new_page, slot=slot)
        #         if placeholder:
        #             opts = {
        #                 'placeholder': placeholder,
        #                 'plugin_type': plugin_type,
        #                 'language': self.language_code,
        #                 plugin_body: content,
        #             }
        #             add_plugin(**opts)
        return new_page


class CreatePressureForm(WidgetBaseForm):
    action_kind = "pressure"