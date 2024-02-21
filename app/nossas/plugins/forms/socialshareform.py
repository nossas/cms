from django import forms

from nossas.plugins.models.socialsharemodel import SocialSharePluginModel

class SocialShareIconSelect(forms.CheckboxSelectMultiple):
    template_name = "design/fields/multiple_svg_select.html"
    option_template_name = "design/fields/multiple_svg_select_option.html"

    class Media:
        css = {"all": ("djangocms_frontend/css/button_group.css",)}


class SocialSharePluginForm(forms.ModelForm):
    selected_social_media = forms.MultipleChoiceField(choices=[
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('whatsapp', 'WhatsApp'),
        ('linkedin', 'LinkedIn'),
    ], widget=SocialShareIconSelect, required=False)

    class Meta:
        model = SocialSharePluginModel
        fields = ['title', 'selected_social_media']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['selected_social_media'].initial = self.instance.get_selected_social_media_list()

    def clean_selected_social_media(self):
        return ','.join(self.cleaned_data['selected_social_media'])
