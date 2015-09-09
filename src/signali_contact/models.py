from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, Avg, Case, When, Q
from django.db.models.functions import Coalesce

from contact.models import BaseContactPoint, ContactPointManager, BaseOrganisation
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin
from contact_feedback.models import ContactPointFeedback, ContactPointFeedbackedMixin, ContactPointFeedbackManager


class SignalContactPointManager(ContactPointManager, VisibilityManagerMixin):

    @staticmethod
    def add_public_requirement(queryset):
        return VisibilityManagerMixin.add_public_requirement(queryset).exclude(Q(slug=None) | Q(slug=""))

    def _transform_criteria_base(self, queryset):
        return self.add_public_requirement(queryset)

    def _apply_criteria_sorting(self, queryset, sorting, score_expression):
        queryset, order_by = super()._apply_criteria_sorting(queryset, sorting, score_expression)
        sorting_match_found = False

        # popularity
        if sorting == 'popularity' or sorting == '-popularity':
            sorting_match_found = True
            order_by.insert(0, sorting)

        # new
        if sorting == '-created_at':
            sorting_match_found = True
            order_by.insert(0, sorting)

        # rating
        if sorting == '-rating':
            sorting_match_found = True
            order_by.insert(0, sorting)
            queryset = self.add_average_rating(queryset)

        # effectiveness
        if sorting == '-effective':
            sorting_match_found = True
            order_by.insert(0, sorting)
            queryset = self.add_effectiveness(queryset)

        # ease of use
        if sorting == '-accessibility':
            sorting_match_found = True
            order_by.insert(0, sorting)
            queryset = self.add_accessibility(queryset)

        # visits
        if sorting == '-visits':
            sorting_match_found = True
            order_by.insert(0, sorting)

        if sorting_match_found and '-score' in order_by:
            order_by.remove('-score')

        return queryset, order_by


    def get_by_slug(self, slug):
        query = self.public_base().filter(slug=slug)
        return self.add_prefetch(query)[0]

    def visited_last(self):
        return self.add_prefetch(self.public_base()).order_by('-created_at')

    def added_last(self):
        return self.add_prefetch(self.public_base()).order_by('-created_at')

    def most_effective(self):
        query = self.public_base()
        return self.add_effectiveness(query).order_by('-effective')

    def most_accessible(self):
        query = self.public_base()
        return self.add_accessibility(query).order_by('-accessibility')

    def rated_best(self):
        query = self.public_base()
        return self.add_average_rating(query).order_by('-rating')

    @staticmethod
    def add_prefetch(queryset):
        return queryset.select_related('organisation', 'category') \
            .prefetch_related('keywords')

    @staticmethod
    def add_average_rating(queryset):
        return queryset.annotate(
            rating=Case(
                When(
                    feedback__is_public=True,
                    then=Coalesce(Avg('feedback__rating'), 0)
                ), default=0)
        )

    @staticmethod
    def add_effectiveness(queryset):
        return queryset.annotate(
            effective=Count(
                Case(
                    When(
                        Q(feedback__is_effective=True, feedback__is_public=True),
                        then=1
                    ), default=None)
            ))

    @staticmethod
    def add_accessibility(queryset):
        return queryset.annotate(
            accessibility=Count(
                Case(
                    When(
                        Q(feedback__is_easy=True, feedback__is_public=True),
                        then=1
                    ), default=None)
            ))



class SignalOrganisationManager(models.Manager, VisibilityManagerMixin):
    pass


class Organisation(BaseOrganisation, SignalVisibilityMixin):
    objects = SignalOrganisationManager()


class ContactPoint(BaseContactPoint, SignalVisibilityMixin, ContactPointFeedbackedMixin):
    objects = SignalContactPointManager()
    visits = models.PositiveIntegerField(_('visits'), default=0)

    def rating(self):
        return self.feedback.aggregate(average_rating=models.Avg('rating'))["average_rating"]


class SignaliContactPointFeedbackManager(ContactPointFeedbackManager):
    pass

class SignalContactPointFeedback(ContactPointFeedback):
    objects = SignaliContactPointFeedbackManager()
