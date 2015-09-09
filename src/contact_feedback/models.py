from django.db import models
from django.db.models import Avg, Q
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from .apps import setting


class ContactPointFeedbackedMixin(models.Model):
    class Meta:
        abstract = True


class ContactPointFeedbackManager(models.Manager):

    @staticmethod
    def add_public_requirement(queryset):
        return queryset.filter(is_public=True)

    def public_base(self):
        return self.add_public_requirement(self.all())

    def published(self, user=None):
        if user is None or user.is_anonymous():
            base = self.public_base()
        else:
            base = self.filter(Q(is_public=True) | Q(user=user))
        return base.order_by('-added_at').select_related('user')


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
    is_public = models.BooleanField(_('is public'), default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="feedback_given", verbose_name=_("user"))
    added_at = models.DateTimeField(_('Added at'), default=timezone.now)
    is_effective = models.BooleanField(_("Are you happy with the results of your contact?"), default=False)
    is_easy = models.BooleanField(_("Was it easy to operate with the contact point?"), default=False)
    rating = models.PositiveIntegerField(verbose_name=_("Overall rating"), choices=PERFORMANCE_CHOICES, blank=False, default=0)
    comment = models.TextField(_('description'), null=True, blank=True)
    contactpoint = models.ForeignKey(setting('CONTACT_POINT_MODEL', noparse=True), related_name='feedback')
