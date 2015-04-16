from django.db import models
from django.utils.translation import ugettext_lazy as _


class Setting(models.Model):
    class Meta:
        verbose_name = _('settting')
        verbose_name_plural = _('setttings')

    title = models.CharField(_('title'), max_length=250, blank=False)
    description = models.CharField(_('description'), max_length=250, blank=False)
    google_analytics = models.CharField(_('description'), max_length=250, blank=False)

