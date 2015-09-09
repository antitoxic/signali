from django import forms
from django.db.models import IntegerField
from django.db.models.expressions import RawSQL, Q

from contact.forms import BaseUserCriteriaForm, BaseContactPointForm, make_score_value
from signali_location.models import Area
from .models import ContactPoint

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
            featured_filter = Q(is_featured=self.cleaned_data['is_featured'])
            filters = filters | featured_filter
            score += make_score_value(featured_filter)

        return score, filters & Q(is_public=True)

    def keywords_search_expressions(self):
        if not self.cleaned_data['keywords'].exists():
            return
        contactpoint_table = ContactPoint._meta.db_table
        keywords_through_table = ContactPoint.keywords.through._meta.db_table
        filters = Q()
        if self.cleaned_data['keywords_exact_match']:
            filters = Q(keywords__id__in=list(self.cleaned_data['keywords']))
        ids = self.cleaned_data['keywords'].values_list('pk', flat=True)
        self.max_score += len(ids)
        score = RawSQL(
            'SELECT COUNT(*) FROM {from_table} WHERE keyword_id IN ({id_list}) AND contactpoint_id = {contactpoint_table}.id '.format(
                from_table=keywords_through_table,
                contactpoint_table=contactpoint_table,
                id_list=','.join(str(id) for id in ids)
            ),
            [], output_field=IntegerField()
        )
        return score, filters




class ContactPointForm(BaseContactPointForm):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if instance is not None:
            instance.is_public = False

