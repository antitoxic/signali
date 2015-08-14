from django import forms
from django.db.models import Q

from taxonomy.models import Category, Keyword
from location.models import Area

class UserCriteriaForm(forms.Form):
    start = forms.IntegerField(required=False, min_value=0, initial=0)
    limit = forms.IntegerField(required=False, min_value=1, initial=20)
    sorting = forms.CharField(required=False, initial='title')
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), required=False)
    keywords = forms.ModelMultipleChoiceField(Keyword.objects.all(), required=False)
    areas = forms.ModelMultipleChoiceField(Area.objects.all(), required=False)

    # flags
    category_or_keyword = forms.BooleanField(required=False, initial=False)

    # use initial values as defaults if not provided
    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        return cleaned_data

    def get_instance_fieldname(self, instance):
        if isinstance(instance, Category):
            return 'categories'
        if isinstance(instance, Keyword):
            return 'keywords'

    def get_sorting(self):
        return self.cleaned_data['sorting']

    def get_start(self):
        return self.cleaned_data['start']

    def get_limit(self):
        return self.cleaned_data['limit']

    def to_filters(self):
        filters = Q()
        data = self.cleaned_data
        if data['categories'].exists():
            category_filter = Q(category__in=list(data['categories']))
        if data['keywords'].exists():
            keyword_filter = Q(keywords__in=list(data['keywords']))
        if data['areas'].exists():
            area_filter = Q(operational_area__in=list(data['areas']))

        try:
            if data['category_or_keyword']:
                taxonomy_filter = category_filter | keyword_filter
            else:
                taxonomy_filter = category_filter & keyword_filter

            filters = filters & taxonomy_filter
        except UnboundLocalError:
            try:
                filters = filters & category_filter
            except UnboundLocalError:
                pass

            try:
                filters = filters & keyword_filter
            except UnboundLocalError:
                pass

        try:
            filters = filters & area_filter
        except UnboundLocalError:
            pass

        return filters

