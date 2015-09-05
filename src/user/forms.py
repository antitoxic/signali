from django import forms
from django.contrib.auth import get_user_model

from security.forms import SetPasswordForm


class SignUpForm(SetPasswordForm):
    email = forms.EmailField(required=True)

class SignUpCheckpointForm(forms.Form):
    fullname = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    def clean(self):
        data = self.cleaned_data
        try:
            data['first_name'], data['last_name'] = data['fullname'].strip().split(' ', 1)
        except:
            data['first_name'] = data['fullname']
            data['last_name'] = ''
        return data

class ProfileUpdateForm(SignUpCheckpointForm, SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].required = False
        self.fields['new_password2'].required = False

    def clean_new_password2(self):
        if not self.cleaned_data.get('new_password1'):
            return self.cleaned_data.get('new_password2')

        return super().clean_new_password2()

    def clean(self):
        data = self.cleaned_data
        if data['new_password1']:
            data['password'] = data['new_password1']
        data['first_name'], data['last_name'] = data['fullname'].strip().split(' ', 1)
        return data

class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserFormNoPassword(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name']
