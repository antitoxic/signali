from django import forms
from django.db.models import IntegerField
from django.db.models.expressions import RawSQL, Q

from contact.forms import BaseUserCriteriaForm, BaseContactPointForm, make_score_value
from signali_location.models import Area
from signali_taxonomy.models import Category
from .models import ContactPoint

class UserCriteriaForm(BaseUserCriteriaForm):
    is_featured = forms.BooleanField(required=False)
    SEARCH_SORTING_CHOICES = BaseUserCriteriaForm.SEARCH_SORTING_CHOICES + (
        ('popularity', 'Most unpopular'),
        ('-popularity', 'Most popular'),
        ('-created_at', 'Created last'),
        ('-rating', 'Rated best'),
        ('-effectiveness', 'Most effective'),
        ('-accessibility', 'Most accessible'),
        ('-last_visited_at', 'Last visited'),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["areas"].queryset = Area.objects.non_address()
        self.fields["categories"].queryset = Category.objects.public().children().non_empty()
        self.fields["sorting"].choices = self.SEARCH_SORTING_CHOICES


    """
    If we want we can annotate match_<fieldname>_<id> with django.db.models.Value() and know which
    field we did match, but that's easily determined from each single result
    """
    def to_search_expressions(self):
        score, filters, term = super().to_search_expressions()
        if 'is_featured' in self.data:
            featured_filter = Q(is_featured=self.cleaned_data['is_featured'])
            if self.is_narrow:
                filters = filters & featured_filter
            score += make_score_value(featured_filter)
            self.max_score += 1

        if self.has_specific_area():
            filters = filters & ~Q(parent=None)
        else:
            filters = filters & Q(parent=None)

        return score, filters & Q(is_public=True), term

    def keywords_score(self):
        if not self.cleaned_data['keywords'].exists():
            return 0
        contactpoint_table = ContactPoint._meta.db_table
        keywords_through_table = ContactPoint.keywords.through._meta.db_table
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
        return score




class ContactPointForm(BaseContactPointForm):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["operational_area"].queryset = Area.objects.non_address()

        if instance is not None:
            instance.is_public = False

