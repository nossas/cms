from cms.plugin_base import CMSPluginBase

from .models import Community

from contrib.actions.pressure.forms import CreatePressurePluginForm, EditPressurePluginForm


class BondeWidgetPluginBase(CMSPluginBase):
    edit_form_class = EditPressurePluginForm
    add_form_class = CreatePressurePluginForm

    def get_form(self, request, obj=None, **kwargs):
        if obj and obj.reference_id:
            form_class = self.edit_form_class
        else:
            form_class = self.add_form_class

        kwargs['form'] = form_class

        form = super(BondeWidgetPluginBase, self).get_form(request, obj, **kwargs)

        # Configura valores iniciais
        if form_class == self.add_form_class:
            c = Community.objects.on_site(request).first()
            if c:
                form.base_fields['community_id'].initial = c.id

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