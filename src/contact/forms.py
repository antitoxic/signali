from django import forms
from django.db.models import Q
from .apps import setting

ContactPoint = setting("CONTACT_POINT_MODEL")
Category = setting("CONTACT_CATEGORY_MODEL")
Keyword = setting("CONTACT_KEYWORD_MODEL")
Area = setting("CONTACT_AREA_MODEL")

class BaseUserCriteriaForm(forms.Form):
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



FeedbackModel = setting("CONTACT_FEEDBACK_MODEL")


class BaseContactPointForm(forms.ModelForm):
    class Meta:
        model = ContactPoint
        fields = (
            "title",
            "url",
            "category",
            "notes",
            "operational_area",
            # "keywords",
            "proposed_by",
            # features:
            "is_multilingual",
            "is_response_guaranteed",
            "is_verifiable",
            "is_confirmation_issued",
            "is_mobile_friendly",
            "is_final_destination",
            "is_anonymous_allowed",
            # requirements:
            "is_registration_required",
            "is_photo_required",
            "is_esign_required",
            "is_name_required",
            "is_email_required",
            "is_pic_required",
            "is_address_required",
            "is_location_required",
        )
        widgets = {
            'proposed_by': forms.HiddenInput(),
        }

    force_required = ["title", "url", "category", "notes", "operational_area"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for fieldname in self.fields:
            if fieldname in self.force_required:
                self.fields[fieldname].required = True



def get_contactpoint_from(data=None, initial=None, prefix=None):
    instance = ContactPoint()
    FormClass = setting('CONTACT_POINT_FORM', BaseContactPointForm)
    return FormClass(data=data,
                     initial=initial,
                     instance=instance,
                     prefix=prefix)
