from django import forms
from bleach import clean
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ("email",)

    def clean_comment(self):
        return clean(self.cleaned_data['comment'])


def get_subscriber_form(contactpoint, data=None, initial=None, prefix=None):
    instance = Subscriber(contactpoint=contactpoint)
    return SubscriberForm(data=data,
                     initial=initial,
                     instance=instance,
                     prefix=prefix)
