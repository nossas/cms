from django import forms

from .widgets import ActionSelectWidget, ActionChoices


class ReferenceBaseForm(forms.ModelForm):
    """ """

    class Meta:
        abstract = True
        fields = ["reference_id"]

    class Media:
        js = ("//ajax.googleapis.com/ajax/libs/jquery/3.7.0/jquery.min.js",)

    reference_id = forms.ChoiceField(
        label="Selecione a widget criada no BONDE",
        widget=ActionSelectWidget,
        required=False,
    )

    action_kind = None

    def __init__(self, *args, **kwargs):
        super(ReferenceBaseForm, self).__init__(*args, **kwargs)

        # Configurar tipo de ação para filtrar widgets
        self.fields["reference_id"].choices = ActionChoices(self.action_kind)
