from django.db import models
from django.db.models import Avg
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


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

    usability = models.PositiveIntegerField(verbose_name=_("Usability"), choices=PERFORMANCE_CHOICES, max_length=2, blank=True, null=True)
    response_speed = models.PositiveIntegerField(verbose_name=_("Response speed"), choices=PERFORMANCE_CHOICES, max_length=2, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="votes", verbose_name=_("voter"))
    added_at = models.DateTimeField(_('added at'), default=timezone.now)
    comment = models.TextField(_('description'), null=True, blank=True)
