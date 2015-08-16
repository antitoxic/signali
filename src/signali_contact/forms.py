from django import forms
from django.db.models import Q
from contact.forms import BaseUserCriteriaForm

class UserCriteriaForm(BaseUserCriteriaForm):
    is_featured = forms.BooleanField(required=False)

    def to_filters(self):
        filters = super().to_filters()
        if 'is_featured' in self.data:
            filters = filters & Q(is_featured=self.cleaned_data['is_featured'])

        return filters & Q(is_public=True)
