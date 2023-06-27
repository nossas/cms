from django import forms


class ChatGPTForm(forms.Form):
    input_text = forms.CharField(required=True, widget=forms.Textarea)