from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class BaseSubscriber(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('subscriber')
        verbose_name_plural = _('subscribers')

    email = models.EmailField(_('email'), max_length=250, blank=False)
    last_notified_at = models.DateTimeField(_('Last notified at'), default=timezone.now)
    created_at = models.DateTimeField(_('Added at'), default=timezone.now)
