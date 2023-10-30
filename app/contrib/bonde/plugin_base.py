from cms.plugin_base import CMSPluginBase

from .models import Community


class BondeWidgetPluginBase(CMSPluginBase):
    edit_form_class = None
    add_form_class = None

    def get_form(self, request, obj, change, **kwargs):
        if obj and not obj.reference_id:
            self.form = self.add_form_class
            form = super().get_form(request, obj, change, **kwargs)
            # Add default values
            c = Community.objects.on_site(request).first()
            form.base_fields["community_id"].initial = c.id
        else:
            self.form = self.edit_form_class
            form = super().get_form(request, obj, change, **kwargs)

        return form

    def get_fieldsets(self, request, obj):
        if obj and obj.reference_id:
            return [
                (
                    "Agradecimento",
                    {
                        "fields": [
                            "sender_name",
                            "sender_email",
                            "email_subject",
                            "email_text",
                        ]
                    },
                ),
                (
                    "Formulário",
                    {
                        "fields": ["title", "button_text", "main_color", "count_text"],
                    },
                ),
                (
                    "Compartilhamento",
                    {
                        "fields": ["whatsapp_text"],
                    },
                ),
            ] + self.fieldsets

        return [
            (None, {"fields": ["reference_id"]}),
            ("Ou cria uma nova widget", {"fields": ["name", "community_id"]}),
        ]