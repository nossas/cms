from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())


class CheckoutForm(forms.Form):
    is_valid = forms.BooleanField()