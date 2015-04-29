from django import forms


class SignUpCheckpointForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)