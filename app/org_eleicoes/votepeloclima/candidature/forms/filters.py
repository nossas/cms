from django import forms
from django.utils.functional import lazy

from crispy_forms.layout import Layout, Div
from crispy_forms.helper import FormHelper
# from django_select2.forms import Select2Widget

from ..layout import NoCrispyField
from ..choices import Gender, Color, Sexuality
from ..fields import CepField, ButtonCheckboxSelectMultiple, ButtonRadioSelect
from ..locations_utils import get_states, get_choices
from ..models import Candidature

from .register import ProposeForm


class RemoveRequiredMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True

        for field_name in self.fields:
            self.fields[field_name].required = False


class FilterFormHeader(RemoveRequiredMixin, forms.ModelForm):
    keyword = forms.CharField(
        label="Buscar por temas ou nomes",
        widget=forms.TextInput(attrs={"placeholder": "Digite um tema ou nome"}),
    )
    state = CepField(
        field="state",
        label="Estado",
        placeholder="Todos os estados",
        choices=[("", "Todos os estados")] + lazy(get_states, list)(),
    )
    city = CepField(
        field="city", parent="state", label="Município", placeholder="Selecione"
    )

    class Meta:
        model = Candidature
        fields = [
            "state",
            "city",
            "intended_position",
            "political_party",
            "keyword",
        ]
        widgets = {
            # "political_party": Select2Widget()
        }

    class Media:
        js = ["https://code.jquery.com/jquery-3.5.1.min.js"]
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        state = self.data.get("state")
        if state:
            self.fields["city"].choices = [("", "Selecione")] + get_choices(state)


class FilterFormSidebar(RemoveRequiredMixin, forms.ModelForm):
    proposes = forms.MultipleChoiceField(
        label="Propostas", widget=ButtonCheckboxSelectMultiple
    )
    mandate_type = forms.ChoiceField(
        label="Tipo de mandato",
        choices=(("", "Todos"), ("individual", "Individual"), ("coletivo", "Mandato coletivo")),
        widget=ButtonRadioSelect,
    )
    gender = forms.MultipleChoiceField(
        label="Gênero", choices=Gender.choices[1:], widget=ButtonCheckboxSelectMultiple
    )
    color = forms.MultipleChoiceField(
        label="Cor ou raça", choices=Color.choices[1:], widget=ButtonCheckboxSelectMultiple
    )
    sexuality = forms.MultipleChoiceField(
        label="Sexualidade", choices=Sexuality.choices[1:], widget=ButtonCheckboxSelectMultiple
    )

    class Meta:
        model = Candidature
        fields = ["proposes", "mandate_type", "gender", "color", "sexuality"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["proposes"].choices = self.get_proposes_choices()

        self.helper.layout = Layout(
            NoCrispyField("proposes"),
            NoCrispyField("mandate_type"),
            NoCrispyField("gender"),
            NoCrispyField("color"),
            NoCrispyField("sexuality"),
        )

    def get_proposes_choices(self):
        form = ProposeForm()
        choices = []
        for field_name in form.fields:
            if field_name != "properties":
                choices.append((field_name, form.fields[field_name].checkbox_label))

        return choices


class FilterFactoryForm(object):

    def __init__(self, data=None):
        self._errors = {}
        self.data = data

        self.header = FilterFormHeader(self.data)
        self.sidebar = FilterFormSidebar(self.data)

    def is_valid(self):
        is_valid = True

        if not self.header.is_valid():
            is_valid = False
            self._errors.update(self.header.errors)

        if not self.sidebar.is_valid():
            is_valid = False
            self._errors.update(self.sidebar.errors)

        return is_valid

    @property
    def errors(self):
        return self._errors if len(self._errors) > 0 else None

    @property
    def cleaned_data(self):
        return {**self.header.cleaned_data, **self.sidebar.cleaned_data}
