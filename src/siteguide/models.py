from django.db import models
from django.utils import timezone
from redactor.fields import RedactorField
from django.utils.translation import ugettext_lazy as _


class Setting(models.Model):
    class Meta:
        verbose_name = _('settting')
        verbose_name_plural = _('setttings')

    title = models.CharField(_('title'), max_length=250, blank=False)
    description = models.CharField(_('description'), max_length=250, blank=False)
    google_analytics = models.CharField(_('description'), max_length=250, blank=False)


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Заглавие'))
    slug = models.SlugField(max_length=255, verbose_name=_('URL част'))
    contents = RedactorField(verbose_name=_('Съдържание'))
    created_at = models.DateTimeField(_('added at'), default=timezone.now)
    changed_at = models.DateTimeField(_('added at'), default=timezone.now)
    is_public = models.BooleanField(default=False, verbose_name=_('Публикувана'))
    style = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Стил [технически]'))
