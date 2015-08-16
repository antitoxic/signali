from django.db import models

from contact.models import BaseContactPoint, ContactPointManager, BaseOrganisation
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin
from contact_feedback.models import ContactPointFeedback, ContactPointFeedbackedMixin


class SignalContactPointManager(ContactPointManager, VisibilityManagerMixin):
    def _apply_criteria_sorting(self, queryset, sorting):
        if sorting == 'popularity':
            return queryset.order_by('popularity')
        return super()._apply_criteria_sorting(queryset, sorting)

class SignalOrganisationManager(models.Manager, VisibilityManagerMixin):
    pass


class Organisation(BaseOrganisation, SignalVisibilityMixin):
    objects = SignalOrganisationManager()

class ContactPoint(BaseContactPoint, SignalVisibilityMixin, ContactPointFeedbackedMixin):
    objects = SignalContactPointManager()


class SignalContactPointFeedback(ContactPointFeedback):
    contactpoint = models.ForeignKey('ContactPoint', related_name='feedback')
