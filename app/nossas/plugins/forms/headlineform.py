from django import forms

class HeadlineIconSelect(forms.RadioSelect):
    template_name = "design/fields/svg_select.html"
    option_template_name = "design/fields/svg_select_option.html"

    class Media:
        css = {"all": ("djangocms_frontend/css/button_group.css",)}


class HeadlineForm(forms.ModelForm):

    class Meta:
        widgets = {"icon": HeadlineIconSelect}
