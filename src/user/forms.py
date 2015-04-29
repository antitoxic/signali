from django import forms
from security.forms import SetPasswordForm


class SignUpForm(SetPasswordForm):
    email = forms.EmailField(required=True)

class SignUpCheckpointForm(forms.Form):
    fullname = forms.CharField(required=True)
    email = forms.EmailField(required=True)

class ProfileUpdateForm(SignUpCheckpointForm, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

    def clean_new_password2(self):
        if not self.cleaned_data.get('new_password1'):
            return self.cleaned_data.get('new_password2')

        return super().clean_new_password2()