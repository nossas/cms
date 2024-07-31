import sys

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import filesizeformat

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
            + ["js/cep-fields.js"],
            css={"screen": select2_css},
        )


class CepField(forms.ChoiceField):

    def __init__(self, field, parent=None, *args, **kwargs):
        placeholder = kwargs.pop("placeholder", None)
        widget_attrs = {
            "data-address-name": field,
            "data-address-url": reverse_lazy("address"),
            "data-address-placeholder": placeholder,
        }
        if parent:
            widget_attrs.update({"data-address-parent": parent})

        self.widget = CepWidget(attrs=widget_attrs)

        super().__init__(**kwargs)

    def valid_value(self, value):
        is_valid = super().valid_value(value)
        if self.choices:
            return is_valid

        return True


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
        self.help_text = help_text
        super().__init__(attrs=attrs)

    def get_context(self, name, value, attrs):
        attrs = {"rows": 4, **(attrs or {})}
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


class CheckboxTextWidget(forms.MultiWidget):

    def __init__(
        self,
        checkbox_label,
        text_label=None,
        text_help_text=None,
        help_text=None,
        attrs=None,
    ):
        widgets = [
            SwitchInput(
                attrs={"data-checktext": ""}, label=checkbox_label, help_text=help_text
            ),
            TextareaInput(attrs=attrs, label=text_label, help_text=text_help_text),
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

    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        if "disabled" in self.attrs and self.attrs["disabled"] and not value:
            return self._render("forms/widgets/nop.html", context, renderer)
        return self._render(self.template_name, context, renderer)

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
        text_help_text=None,
        max_length=None,
        min_length=None,
        strip=True,
        empty_value="",
        help_text=None,
        **kwargs,
    ):
        self.widget = CheckboxTextWidget(
            checkbox_label=checkbox_label,
            text_label=text_label,
            text_help_text=text_help_text,
            help_text=help_text,
        )

        super().__init__(
            max_length=None, min_length=None, strip=True, empty_value="", **kwargs
        )
        # Remove label to use only subwidgets label
        self.label = ""

    def validate(self, value):
        value = value or ""
        text_value = value.replace("on-", "")
        if value.startswith("on-") and not text_value:
            raise ValidationError(_("Required"))

    def clean(self, value):
        value = super().clean(value)
        return value.replace("on-", "")

    # def get_bound_field(self, form, field_name):
    #     bound_field = super().get_bound_field(form ,field_name)
    #     if self.disabled:
    #         import ipdb;ipdb.set_trace()
    #     return bound_field


class InlineArrayWidget(forms.MultiWidget):
    template_name = "forms/widgets/inline_array.html"

    def __init__(self, widget, size, item_label=None, add_button_text=None, attrs=None):
        self.add_button_text = add_button_text
        self.item_label = item_label
        widgets = [
            widget() if isinstance(widget, type) else widget for _ in range(size)
        ]
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
        return [v.strip() for v in value.split(",")]

    def value_from_datadict(self, data, files, name):
        values = []
        for key, value in data.items():
            if key.startswith(f"{name}_"):
                values.append(value)
        return values

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        invalid_count = len(
            list(
                filter(
                    lambda x: "is-invalid" in x.get("attrs", {}).get("class", ""),
                    context["widget"]["subwidgets"],
                )
            )
        )
        context["widget"].update(
            {
                "item_label": self.item_label,
                "add_button_text": self.add_button_text,
                "size": self.size,
                "attrs": (
                    {**context["widget"]["attrs"], "class": "is-invalid"}
                    if invalid_count > 0
                    else context["widget"]["attrs"]
                ),
            }
        )

        return context


class ChangeHelpTextBoundField(forms.BoundField):
    def __str__(self):
        help_text_html = (
            f"<div class='form-text mb-3'>{self.field.add_help_text}</div>"
            if self.field.add_help_text
            else ""
        )
        widget_html = self.as_widget()
        return f"{help_text_html}{widget_html}"


class NoLabelBoundField(forms.BoundField):
    def label_tag(self, contents=None, attrs=None, label_suffix=None):
        return ""


class InlineArrayField(SimpleArrayField):
    def __init__(
        self,
        base_field,
        size=5,
        item_label=None,
        add_button_text=None,
        delimiter=",",
        max_length=None,
        min_length=None,
        **kwargs,
    ):
        self.add_help_text = kwargs.pop("help_text", None)
        super().__init__(
            base_field,
            delimiter=delimiter,
            max_length=max_length,
            min_length=min_length,
            **kwargs,
        )
        self.widget = InlineArrayWidget(
            widget=base_field.widget,
            size=size,
            item_label=item_label,
            add_button_text=add_button_text,
        )

    def get_bound_field(self, form, field_name):
        return ChangeHelpTextBoundField(form, self, field_name)


class ToogleButtonInput(forms.CheckboxInput):
    template_name = "forms/widgets/toggle_button.html"

    @property
    def media(self):
        return forms.Media(css={"screen": ["css/icons.css"]})

    def __init__(self, text_html, icon_name=None, *args, **kwargs):
        self.text_html = text_html
        self.icon_name = icon_name
        super().__init__(*args, **kwargs)

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        context["widget"].update(
            {
                "text_html": self.text_html,
                "icon_name": self.icon_name,
                "attrs": {**context["widget"].get("attrs", {}), "class": "btn-check"},
            }
        )

        return context


class ToggleButtonField(forms.BooleanField):

    def __init__(self, text_html, icon_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.widget = ToogleButtonInput(text_html=text_html, icon_name=icon_name)

    def get_bound_field(self, form, field_name):
        """
        Return a BoundField instance that will be used when accessing the form
        field in a template.
        """
        return NoLabelBoundField(form, self, field_name)


class FileInput(forms.ClearableFileInput):
    template_name = "forms/widgets/file_input.html"


class ImageField(forms.ImageField):
    widget = FileInput


class VideoField(forms.FileField):
    widget = FileInput
    default_validators = [
        FileExtensionValidator(
            allowed_extensions=["MOV", "avi", "mp4", "webm", "mkv"],
            message="Tipo de arquivo não suportado.",
        )
    ]

    def __init__(
        self, *, max_size=50, max_length=None, allow_empty_file=False, **kwargs
    ):
        super().__init__(
            max_length=max_length, allow_empty_file=allow_empty_file, **kwargs
        )
        # 50MB
        self.max_size = max_size * 1024 * 1024
        self.widget.attrs["accept"] = "video/*"

    def clean(self, value, initial):
        value = super().clean(value, initial)
        if value:
            content_type = getattr(value, "content_type", None)
            if not content_type:
                import mimetypes

                content_type, _ = mimetypes.guess_type(value.file.name)

            if "video" in content_type:
                if value.size > self.max_size:
                    raise forms.ValidationError(
                        "Por favor, escolha um video com tamanho de até %s. Tamanho Atual %s"
                        % (filesizeformat(self.max_size), filesizeformat(value.size))
                    )

        return value
