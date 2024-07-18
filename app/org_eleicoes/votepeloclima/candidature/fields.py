import sys

from django import forms
from django.conf import settings
from django.urls import reverse_lazy

from django_select2.forms import Select2Widget
from captcha.fields import ReCaptchaField


class ValidateOnceReCaptchaField(ReCaptchaField):
    def clean(self, values):
        # find the 'revalidating' value in stack
        frame = sys._getframe()
        max_depth = 25
        while frame and max_depth != 0:
            if "revalid" in frame.f_locals:
                return values[0]
            max_depth -= 1
            frame = frame.f_back
        return super(ValidateOnceReCaptchaField, self).clean(values)


class CepWidget(Select2Widget):

    @property
    def media(self):
        """
        Construct Media as a dynamic property.

        .. Note:: For more information visit
            https://docs.djangoproject.com/en/stable/topics/forms/media/#media-as-a-dynamic-property
        """
        select2_js = settings.SELECT2_JS if settings.SELECT2_JS else []
        select2_css = settings.SELECT2_CSS if settings.SELECT2_CSS else []

        if isinstance(select2_js, str):
            select2_js = [select2_js]
        if isinstance(select2_css, str):
            select2_css = [select2_css]

        i18n_file = []
        if self.i18n_name in settings.SELECT2_I18N_AVAILABLE_LANGUAGES:
            i18n_file = [f"{settings.SELECT2_I18N_PATH}/{self.i18n_name}.js"]

        return forms.Media(
            js=["https://code.jquery.com/jquery-3.5.1.min.js"]
            + select2_js
            + i18n_file
            + ["django_select2/django_select2.js"]
            + ["js/address-fields.js"],
            css={"screen": select2_css + ["django_select2/django_select2.css"]},
        )


class StateCepField(forms.ChoiceField):
    widget = CepWidget(
        attrs={
            "data-address-fields": "state",
            "data-address-url": reverse_lazy("address"),
        }
    )

    def __init__(self, *args, **kwargs):
        from .locations_utils import get_ufs

        super().__init__(**kwargs)
        self.choices = get_ufs


class CityCepField(forms.CharField):
    widget = CepWidget(
        attrs={
            "data-address-fields": "city",
            "data-address-url": reverse_lazy("address"),
        }
    )


class CheckboxTextWidget(forms.MultiWidget):

    def __init__(self, attrs=None):

        widgets = [
            forms.CheckboxInput(attrs={"data-checktext": ""}),
            forms.Textarea(attrs=attrs)
        ]

        super().__init__(widgets, attrs)
    
    def decompress(self, value):
        if value:
            return [True, value]
        return [False, ""]
    
    def value_from_datadict(self, data, files, name):
        checkbox, text = super().value_from_datadict(data, files, name)
        if checkbox:
            return text
        return None
    
    @property
    def media(self):
        return forms.Media(
            js=["https://code.jquery.com/jquery-3.5.1.min.js", "js/checkbox-text-widget.js"],
            # css={"screen": select2_css + ["django_select2/django_select2.css"]},
        )