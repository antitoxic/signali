from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .apps import setting


class ContactPointFeedbackedMixin(models.Model):
    class Meta:
        abstract = True

    @property
    def usability_score(self):
        return self.feedback.all().aggregate(score=Avg('usability')).score

    @property
    def response_speed_score(self):
        return self.feedback.all().aggregate(score=Avg('response_speed')).score


class ContactPointFeedback(models.Model):
    class Meta:
        abstract = True

    PERFORMANCE_CHOICES = (
        (1, _('Weak')),
        (2, _('Could be better')),
        (3, _('Adequate')),
        (4, _('Good')),
        (5, _('Excellent')),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="feedback_given", verbose_name=_("Voter"))
    added_at = models.DateTimeField(_('Added at'), default=timezone.now)
    is_effective = models.BooleanField(_("Are you happy with the results of your contact?"), default=False)
    is_easy = models.BooleanField(_("Was it easy to operate with the contact point?"), default=False)
    rating = models.PositiveIntegerField(verbose_name=_("Overall rating"), choices=PERFORMANCE_CHOICES, max_length=2, blank=False, null=True)
    comment = models.TextField(_('description'), null=True, blank=True)
    contactpoint = models.ForeignKey(setting('CONTACT_POINT_MODEL', noparse=True), related_name='feedback')
