from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ("user",)


class AnonymousSubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ("email",)


def get_anon_subscriber_form(contactpoint, data=None, initial=None, prefix=None):
    instance = Subscriber(contactpoint=contactpoint)
    return AnonymousSubscriberForm(data=data,
                     initial=initial,
                     instance=instance,
                     prefix=prefix)
