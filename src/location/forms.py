from django import forms
from django_select2.forms import ModelSelect2Widget

class AreaAutosuggestWidget(ModelSelect2Widget):
    search_fields = [
        'title__icontains',
        'size__title__icontains',
    ]
    media = forms.Media()
