from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class BaseSubscriber(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="subscriptions",
        verbose_name=_("user"), null=True, blank=True)
    email = models.EmailField(_('email'), max_length=250, blank=True, null=True)
    last_notified_at = models.DateTimeField(_('Last notified at'), default=timezone.now)
    created_at = models.DateTimeField(_('Added at'), default=timezone.now)
