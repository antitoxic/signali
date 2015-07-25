from django import forms
from taxonomy.models import Category, Keyword
from location.models import Area

class UserCriteria(forms.Form):
    categories = forms.ModelMultipleChoiceField(Category.objects.all(), required=False)
    keywords = forms.ModelMultipleChoiceField(Keyword.objects.all(), required=False)
    area = forms.ModelMultipleChoiceField(Area.objects.all(), required=False)

    def get_instance_fieldname(self, instance):
        if isinstance(instance, Category):
            return 'categories'
        if isinstance(instance, Keyword):
            return 'keywords'
