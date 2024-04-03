from django import forms, VERSION
from django.utils.safestring import mark_safe
from django.forms.utils import flatatt
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _


class CharsLeftTextInput(forms.TextInput):
    def render(self, name, value, attrs=None, **kwargs):
        if value is None:
            value = ""

        extra_attrs = {
            "type": self.input_type,
            "name": name,
            "maxlength": self.attrs.get("maxlength"),
        }

        # Signature for build_attrs changed in 1.11
        # https://code.djangoproject.com/ticket/28095
        if VERSION < (1, 11):
            final_attrs = self.build_attrs(attrs, **extra_attrs)
        else:
            final_attrs = self.build_attrs(attrs, extra_attrs=extra_attrs)

        if value != "":
            final_attrs["value"] = force_str(value)

        maxlength = final_attrs.get("maxlength", False)
        if not maxlength:
            return mark_safe("<input%s />" % flatatt(final_attrs))

        current = force_str(int(maxlength) - len(value))
        html = """
            <span class="charsleft charsleft-input">
            <input %(attrs)s />
            <span>
                <span class="count">%(current)s</span> %(char_remain_str)s</span>
                <span class="maxlength">%(maxlength)s</span>
            </span>
        """ % {
            "attrs": flatatt(final_attrs),
            "current": current,
            "char_remain_str": _("caracteres restantes"),
            "maxlength": int(maxlength),
        }
        return mark_safe(html)

    class Media:
        css = {
            "screen": ("charsleft-widget/css/charsleft.css",),
        }
        js = (
            "https://code.jquery.com/jquery-3.5.1.slim.min.js",
            "charsleft-widget/js/charsleft.js",
        )


class CharsLeftTextarea(forms.Textarea):
    def render(self, name, value, attrs=None, **kwargs):
        if value is None:
            value = ""

        extra_attrs = {
            "name": name,
            "maxlength": self.attrs.get("maxlength"),
        }

        # Signature for build_attrs changed in 1.11
        # https://code.djangoproject.com/ticket/28095
        if VERSION < (1, 11):
            final_attrs = self.build_attrs(attrs, **extra_attrs)
        else:
            final_attrs = self.build_attrs(attrs, extra_attrs=extra_attrs)

        if value != "":
            value = force_str(value)

        maxlength = final_attrs.get("maxlength", False)
        if not maxlength:
            return mark_safe(
                '<textarea  cols="40" rows="10" %(attrs)s>%(value)s</textarea>'
                % {"value": value, "attrs": flatatt(final_attrs)}
            )

        current = force_str(int(maxlength) - len(value))
        html = """
            <span class="charsleft charsleft-input">
            <textarea cols="40" rows="10" %(attrs)s>%(value)s</textarea>
            <span>
                <span class="count">%(current)s</span> %(char_remain_str)s</span>
                <span class="maxlength">%(maxlength)s</span>
            </span>
        """ % {
            "value": value,
            "attrs": flatatt(final_attrs),
            "current": current,
            "char_remain_str": _("caracteres restantes"),
            "maxlength": int(maxlength),
        }
        return mark_safe(html)

    class Media:
        css = {
            "screen": ("charsleft-widget/css/charsleft.css",),
        }
        js = (
            "https://code.jquery.com/jquery-3.5.1.slim.min.js",
            "charsleft-widget/js/charsleft-textarea.js",
        )
