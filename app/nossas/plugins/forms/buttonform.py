from django import forms
from django.conf import settings
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from djangocms_frontend.contrib.link.forms import LinkForm
from djangocms_frontend.fields import ColoredButtonGroup

# from djangocms_frontend import settings
from nossas.design.forms import EMPTY_CHOICES

# from nossas.plugins.models.buttonmodel import Button


CONTEXT_COLORS = EMPTY_CHOICES + [
    (slugify(args[0]), args[0]) for args in settings.DESIGN_THEME_COLORS
]


class MyLinkForm(LinkForm):
    link_context = forms.ChoiceField(
        label=_("Context"),
        choices=CONTEXT_COLORS,
        initial="",
        required=False,
        widget=ColoredButtonGroup(),
    )


#     class Meta:
#         model = Button
#         entangled_fields = {"attributes": []}
