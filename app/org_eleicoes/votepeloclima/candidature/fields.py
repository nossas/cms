import sys

from django import forms
from django.conf import settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from django.contrib.postgres.forms import SimpleArrayField
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


class Select2CustomWidget(Select2Widget):

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
    widget = Select2CustomWidget(
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
    widget = Select2CustomWidget(
        attrs={
            "data-address-fields": "city",
            "data-address-url": reverse_lazy("address"),
        }
    )


class SwitchInput(forms.CheckboxInput):
    template_name = "forms/widgets/switch.html"

    def __init__(self, label, help_text=None, attrs=None):
        self.label = label
        self.help_text = help_text
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context.update(
            {
                "widget": {
                    **context["widget"],
                    "label": self.label,
                    "help_text": self.help_text,
                }
            }
        )
        return context


class TextareaInput(forms.Textarea):
    template_name = "forms/widgets/textarea.html"

    def __init__(self, label=None, help_text=None, attrs=None):
        self.label = label
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        attrs = {"rows": 4, **(attrs or {})}
        context = super().get_context(name, value, attrs)
        context.update({"widget": {**context["widget"], "label": self.label}})
        return context


class CheckboxTextWidget(forms.MultiWidget):

    def __init__(self, checkbox_label, text_label=None, help_text=None, attrs=None):
        widgets = [
            SwitchInput(
                attrs={"data-checktext": ""}, label=checkbox_label, help_text=help_text
            ),
            TextareaInput(attrs=attrs, label=text_label),
        ]

        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            value = value.replace("on-", "")
            return [True, value]
        return [False, ""]

    def value_from_datadict(self, data, files, name):
        checkbox, text = super().value_from_datadict(data, files, name)
        if checkbox:
            return "on-" + text
        return None

    @property
    def media(self):
        return forms.Media(
            js=[
                "https://code.jquery.com/jquery-3.5.1.min.js",
                "js/checkbox-text-widget.js",
            ],
            # css={"screen": select2_css + ["django_select2/django_select2.css"]},
        )


class CheckboxTextField(forms.CharField):
    template_name = "forms/fields/checkbox_text.html"

    def __init__(
        self,
        *,
        checkbox_label,
        text_label=None,
        max_length=None,
        min_length=None,
        strip=True,
        empty_value="",
        help_text=None,
        **kwargs,
    ):
        self.widget = CheckboxTextWidget(
            checkbox_label=checkbox_label, text_label=text_label, help_text=help_text
        )

        super().__init__(
            max_length=None, min_length=None, strip=True, empty_value="", **kwargs
        )

    def validate(self, value):
        value = value or ""
        text_value = value.replace("on-", "")
        if value.startswith("on-") and not text_value:
            raise ValidationError(_("Required"))

    def clean(self, value):
        value = super().clean(value)
        return value.replace("on-", "")


class InlineArrayWidget(forms.MultiWidget):
    template_name = "forms/widgets/inline_array.html"

    def __init__(self, widget, size, attrs=None):
        widgets = [widget() if isinstance(widget, type) else widget for _ in range(size)]
        super().__init__(widgets, attrs)
        self.size = size

    @property
    def media(self):
        return forms.Media(
            js=[
                "https://code.jquery.com/jquery-3.5.1.min.js",
                "js/inline-array-widget.js",
            ],
        )
    
    def decompress(self, value):
        if isinstance(value, list):
            return value
        if value is None:
            return []
        return [v.strip() for v in value.split(',')]

    def value_from_datadict(self, data, files, name):
        values = []
        for key, value in data.items():
            if key.startswith(f'{name}_'):
                values.append(value)
        return values
    
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({'size':self.size})

        return context


class InlineArrayField(SimpleArrayField):
    def __init__(self, base_field, size=5, delimiter=",", max_length=None, min_length=None, **kwargs):
        super().__init__(base_field, delimiter=delimiter, max_length=max_length, min_length=min_length, **kwargs)
        self.widget = InlineArrayWidget(widget=base_field.widget, size=size)