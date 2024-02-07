from django import forms

from django_jsonform.forms.fields import JSONFormField

from ..models.newslettermodel import NewsletterPluginModel

class NewsletterSignUpForm(forms.Form):
    name = forms.CharField(label="Nome Completo", max_length=100)
    email = forms.EmailField(label="E-mail")

class NewsletterPluginForm(forms.ModelForm):
    config = JSONFormField(
        schema={
            "type": "dict",
            "keys": {
                "cached_community_id": {"type": "integer"},
                "mobilization_id": {"type": "integer"},
                "widget_id": {"type": "integer"}
            },
            "required": ["cached_community_id", "mobilization_id", "widget_id"]
        }
    )

    class Meta:
        model = NewsletterPluginModel
        fields = "__all__"
