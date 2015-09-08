from django.db import models

from contact.models import BaseContactPoint, ContactPointManager, BaseOrganisation
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin
from contact_feedback.models import ContactPointFeedback, ContactPointFeedbackedMixin


class SignalContactPointManager(ContactPointManager, VisibilityManagerMixin):
    def public_base(self):
        return super().public_base().exclude(slug=None).exclude(slug="")

    def _apply_criteria_sorting(self, queryset, sorting, score_expression):
        queryset, sorting = super()._apply_criteria_sorting(queryset, sorting, score_expression)
        if sorting == 'popularity' or sorting == '-popularity':
            sorting.append(sorting)
        return queryset, sorting

    def get_by_slug(self, slug):
        return self.filter(slug=slug, is_public=True) \
            .select_related('organisation', 'category') \
            .prefetch_related('keywords')[0]


class SignalOrganisationManager(models.Manager, VisibilityManagerMixin):
    pass


class Organisation(BaseOrganisation, SignalVisibilityMixin):
    objects = SignalOrganisationManager()


class ContactPoint(BaseContactPoint, SignalVisibilityMixin, ContactPointFeedbackedMixin):
    objects = SignalContactPointManager()

    def rating(self):
        return self.feedback.aggregate(average_rating=models.Avg('rating'))["average_rating"]


class ContactPointFeedbackManager(models.Manager):
    def published(self):
        return self.order_by('-added_at').select_related('user')


class SignalContactPointFeedback(ContactPointFeedback):
    objects = ContactPointFeedbackManager()
