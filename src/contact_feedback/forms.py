from django import forms
from .apps import setting
from bleach import clean

FeedbackModel = setting("CONTACT_FEEDBACK_MODEL")


class BaseContactFeedbackForm(forms.ModelForm):
    class Meta:
        model = FeedbackModel
        fields = ("is_effective", "is_easy", "rating", "comment", "user")
        widgets = {
            'user': forms.HiddenInput(),
        }

    def clean_comment(self):
        return clean(self.cleaned_data['comment'])


def get_feedbackfrom(contactpoint, data=None, initial=None, prefix=None):
    instance = FeedbackModel(contactpoint = contactpoint)
    FormClass = setting('CONTACT_FEEDBACK_FORM', BaseContactFeedbackForm)
    return FormClass(data=data,
                     initial=initial,
                     instance=instance,
                     prefix=prefix)
