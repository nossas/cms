from django import forms
from captcha.widgets import ReCaptchaV2Checkbox

from .fields import ValidateOnceReCaptchaField


class CaptchaForm(forms.Form):
        captcha = ValidateOnceReCaptchaField(widget=ReCaptchaV2Checkbox())


class EmailForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput())


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())


class CheckoutForm(forms.Form):
    is_valid = forms.BooleanField()