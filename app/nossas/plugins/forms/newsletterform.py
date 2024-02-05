from django import forms


class NewsletterUserForm(forms.Form):
    name = forms.CharField(label="Nome", max_length=100)
    email = forms.EmailField(label="Email")
