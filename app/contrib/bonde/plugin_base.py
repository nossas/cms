from cms.plugin_base import CMSPluginBase


class BondeWidgetPluginBase(CMSPluginBase):
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

        return [(None, {"fields": ["reference_id"]})]
