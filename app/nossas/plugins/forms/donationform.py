from django import forms


class DonationUserForm(forms.Form):
    name = forms.CharField(label="Nome Completo", max_length=100)
    email = forms.EmailField(label="E-mail")
    whatsapp = forms.CharField(label="Whatsapp", max_length=15)
