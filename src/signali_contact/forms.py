from django import forms
from django.db.models import Q

from contact.forms import BaseUserCriteriaForm, BaseContactPointForm
from signali_location.models import Area

class UserCriteriaForm(BaseUserCriteriaForm):
    is_featured = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["areas"].queryset = Area.objects.non_address()


    """
    If we want we can annotate match_<fieldname>_<id> with django.db.models.Value() and know which
    field we did match, but that's easily determined from each single result
    """
    def to_search_expressions(self):
        score, filters = super().to_search_expressions()
        if 'is_featured' in self.data:
            filters = filters & Q(is_featured=self.cleaned_data['is_featured'])

        return score, filters & Q(is_public=True)


class ContactPointForm(BaseContactPointForm):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if instance is not None:
            instance.is_public = False

