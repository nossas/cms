from django import forms


class PressureForm(forms.Form):
    # People Fields
    email_address = forms.EmailField(
        label="Endereço de email",
        widget=forms.EmailInput(attrs={"placeholder": "Insira seu e-mail"}),
    )

    given_name = forms.CharField(
        label="Primeiro nome",
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "Insira seu nome"}),
    )

    family_name = forms.CharField(
        label="Sobrenome",
        required=False,
        max_length=120,
        widget=forms.TextInput(attrs={"placeholder": "Insira seu sobrenome"}),
    )

    phone_number = forms.CharField(
        label="Whatsapp",
        required=False,
        max_length=15,
        widget=forms.TextInput(attrs={"placeholder": "(DDD) 9 9999-9999"}),
    )

    # Action Fields
    email_subject = forms.CharField(label="Assunto", max_length=100, disabled=True)

    email_body = forms.CharField(
        label="Corpo do e-mail", disabled=True, widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        super(PressureForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs[
                "class"
            ] = "input input-sm px-2 rounded-none hover:border-none focus:border-none focus:outline-none"

            if isinstance(visible.field.widget, forms.Textarea):
                visible.field.widget.attrs["class"] += " h-28"
