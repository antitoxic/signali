from django import forms
from django.db.models import IntegerField, Case, When, Q
from .apps import setting

ContactPoint = setting("CONTACT_POINT_MODEL")
Category = setting("CONTACT_CATEGORY_MODEL")
Keyword = setting("CONTACT_KEYWORD_MODEL")
Area = setting("CONTACT_AREA_MODEL")

def make_score_value(filters):
    return Case(When(filters, then=1), default=0, output_field=IntegerField())


class BaseUserCriteriaForm(forms.Form):
    YES = ContactPoint.YES
    NO = ContactPoint.NO
    DONTKNOW = ContactPoint.DONTKNOW
    exact_match_fields = [
        "is_multilingual",
        "is_response_guaranteed",
        "is_verifiable",
        "is_confirmation_issued",
        "is_mobile_friendly",
        "is_final_destination",
        "is_anonymous_allowed",
        "is_registration_required",
        "is_photo_required",
        "is_esign_required",
        "is_name_required",
        "is_email_required",
        "is_pic_required",
        "is_address_required",
        "is_location_required",
    ]
    start = forms.IntegerField(required=False, min_value=0, initial=0)
    limit = forms.IntegerField(required=False, min_value=1, initial=12)
    sorting = forms.CharField(required=False, initial='-score')
    categories = forms.ModelMultipleChoiceField(Category.objects.children().select_related('parent'), required=False)
    keywords = forms.ModelMultipleChoiceField(Keyword.objects.all(), required=False)
    areas = forms.ModelMultipleChoiceField(Area.objects.all(), required=False)

    is_multilingual = forms.ChoiceField(required=False, choices=ContactPoint.EXTENDED_BOOLEAN_CHOICES)
    is_response_guaranteed = forms.ChoiceField(required=False, choices=ContactPoint.EXTENDED_BOOLEAN_CHOICES)
    is_verifiable = forms.ChoiceField(required=False, choices=ContactPoint.EXTENDED_BOOLEAN_CHOICES)
    is_confirmation_issued = forms.ChoiceField(required=False, choices=ContactPoint.EXTENDED_BOOLEAN_CHOICES)
    is_mobile_friendly = forms.ChoiceField(required=False, choices=ContactPoint.EXTENDED_BOOLEAN_CHOICES)
    is_final_destination = forms.ChoiceField(required=False, choices=ContactPoint.EXTENDED_BOOLEAN_CHOICES)
    is_anonymous_allowed = forms.ChoiceField(required=False, choices=ContactPoint.EXTENDED_BOOLEAN_CHOICES)

    is_registration_required = forms.BooleanField(required=False)
    is_photo_required = forms.BooleanField(required=False)
    is_esign_required = forms.BooleanField(required=False)
    is_name_required = forms.BooleanField(required=False)
    is_email_required = forms.BooleanField(required=False)
    is_pic_required = forms.BooleanField(required=False)
    is_address_required = forms.BooleanField(required=False)
    is_location_required = forms.BooleanField(required=False)

    # flags
    category_and_keyword_match = forms.BooleanField(required=False, initial=False)
    category_exact_match = forms.BooleanField(required=False, initial=False)
    keywords_exact_match = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_score = 0

    # use initial values as defaults if not provided
    def clean(self):
        cleaned_data = super().clean()
        for name in self.fields:
            if not self[name].html_name in self.data and self.fields[name].initial is not None:
                cleaned_data[name] = self.fields[name].initial
        return cleaned_data

    def get_instance_html_name(self, instance):
        if isinstance(instance, Category):
            return self["categories"].html_name
        if isinstance(instance, Keyword):
            return self["keywords"].html_name

    def get_sorting(self):
        return self.cleaned_data['sorting']

    def get_start(self):
        return self.cleaned_data['start']

    def get_limit(self):
        return self.cleaned_data['limit']

    def keywords_search_expressions(self):
        raise NotImplementedError('Must implement')

    def categories_search_expressions(self):
        if not self.cleaned_data['categories'].exists():
            return
        filters = Q()
        ids = list(self.cleaned_data['categories'].values_list('pk', flat=True))
        self.max_score += len(ids)
        category_filters = Q(category__id__in=ids)
        if self.cleaned_data['category_exact_match']:
            filters = category_filters
        return make_score_value(category_filters), filters

    """
    If we want we can annotate match_<fieldname>_<id> with django.db.models.Value() and know which
    field we did match, but that's easily determined from each single result
    """
    def to_search_expressions(self):
        score = 0
        data = self.cleaned_data

        try:
            category_score, category_filter = self.categories_search_expressions()
            score += category_score
        except:
            category_filter = Q()

        try:
            keyword_score, keyword_filter = self.keywords_search_expressions()
            score += keyword_score
        except:
            keyword_filter = Q()

        if data['category_and_keyword_match']:
            filters = category_filter & keyword_filter
        else:
            filters = category_filter | keyword_filter

        if data['areas'].exists():
            first_area = data['areas'][0]
            ids = list(first_area.get_ancestors().values_list('pk', flat=True))
            ids = ids + list(data['areas'].values_list('pk', flat=True))
            filters = filters & Q(operational_area__in=ids)
            self.max_score += 1

        for fieldname in self.exact_match_fields:
            if fieldname in self.data:
                score += make_score_value(Q(**{fieldname: self.cleaned_data[fieldname]}))
                self.max_score += 1

        return score, filters




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
    FormClass = setting('CONTACT_POINT_FORM')
    return FormClass(data=data,
                     initial=initial,
                     instance=instance,
                     prefix=prefix)
