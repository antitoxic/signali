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
    areasize_address = models.ForeignKey('location.AreaSize',
                                         verbose_name=_('Which size denotes address-level area'),
                                         blank=False)

    @property
    def contact_address_areasize(self):
        return self.areasize_address


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('URL part'))
    contents = RedactorField(verbose_name=_('Content'))
    created_at = models.DateTimeField(_('Added at'), default=timezone.now)
    changed_at = models.DateTimeField(_('Added at'), default=timezone.now)
    is_public = models.BooleanField(default=False, verbose_name=_('Published'))
    style = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Style [technical]'))
