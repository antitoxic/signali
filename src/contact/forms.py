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
    SEARCH_EXPRESSION_SORTING = '-score'
    SEARCH_EXPRESSION_TAXONOMY_SORTING = '-taxonomy_score'
    SEARCH_SORTING_CHOICES = (
        (SEARCH_EXPRESSION_SORTING, 'Order by search relevance'),
    )
    SEARCH_RANKING_SORTING = '-watson_rank'

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
    sorting = forms.ChoiceField(required=False, initial=SEARCH_EXPRESSION_SORTING, choices=(SEARCH_SORTING_CHOICES,))
    categories = forms.ModelMultipleChoiceField(Category.objects.children().prefetch_parent(), required=False)
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

    def get_sorting(self, score_expressions, score_field=SEARCH_RANKING_SORTING):
        sorting = self.cleaned_data['sorting']
        initial_sorting = self.fields["sorting"].initial
        if sorting == initial_sorting and score_expressions == 0:
            sorting = []
        else:
            sorting = [sorting]
        if self.has_taxonomy():
            if sorting == initial_sorting:
                sorting.insert(0, score_field)
            else:
                sorting.append(score_field)
        return sorting


    def get_start(self):
        return self.cleaned_data['start']

    def get_limit(self):
        return self.cleaned_data['limit']

    def keywords_score(self):
        raise NotImplementedError('Must implement')

    def categories_score(self):
        if not self.cleaned_data['categories'].exists():
            return 0
        ids = list(self.cleaned_data['categories'].values_list('pk', flat=True))
        self.max_score += len(ids)
        return make_score_value(Q(category__id__in=ids))

    def get_area_ids(self):
        first_area = self.cleaned_data['areas'][0]
        ids = list(first_area.get_family().values_list('pk', flat=True))
        ids = ids + list(self.cleaned_data['areas'].values_list('pk', flat=True))
        return set(ids)

    def has_specific_area(self):
        area = self.cleaned_data['areas']
        return area.exists() and not area[0].is_root_node()

    def has_taxonomy(self):
        data = self.cleaned_data
        return data['categories'].exists() or data['keywords'].exists()

    # Kept different from has_taxonomy because `areas` are very likely to be included after user-testing
    @property
    def is_narrow(self):
        return self.has_taxonomy()

    @property
    def is_detailed(self):
        for fieldname in self.exact_match_fields:
            if fieldname in self.data:
                return True
        return False

    def area_search_filters(self):
        if self.has_specific_area():
            return Q(operational_area__in=self.get_area_ids())
        else:
            return Q()

    def get_term(self):
        data = self.cleaned_data
        if not self.has_taxonomy():
            return
        term = ''
        if data['categories'].exists():
            term += ' '.join(self.cleaned_data['categories'].values_list('title', flat=True))
        if data['keywords'].exists():
            term = term + ' ' + ' '.join(self.cleaned_data['keywords'].values_list('title', flat=True))
        return term.strip()

    def taxonomy_score(self):
        return self.categories_score() + self.keywords_score()

    """
    If we want we can annotate match_<fieldname>_<id> with django.db.models.Value() and know which
    field we did match, but that's easily determined from each single result
    """
    def to_search_expressions(self):
        filters = self.area_search_filters()
        score = 0
        exact_match_filters = Q()
        is_narrow = self.is_narrow
        for fieldname in self.exact_match_fields:
            if fieldname in self.data:
                field_filter = Q(**{fieldname: self.cleaned_data[fieldname]})
                score += make_score_value(field_filter)
                self.max_score += 1
                if is_narrow:
                    exact_match_filters = exact_match_filters & field_filter

        filters = filters & exact_match_filters

        return score, filters, self.get_term()


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
        self.fields["category"].queryset = Category.objects.children().select_related('parent')

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
