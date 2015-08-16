from django.db import models
from django.utils.translation import ugettext_lazy as _


class Setting(models.Model):
    class Meta:
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

    title = models.CharField(_('title'), max_length=250, blank=False)
    description = models.CharField(_('description'), max_length=250, blank=False)
    google_analytics = models.CharField(_('google analytics account id'), max_length=250, blank=False)
    areasize_address = models.ForeignKey('signali_location.AreaSize',
                                         verbose_name=_('Which size denotes address-level area'),
                                         blank=False)

    @property
    def contact_address_areasize(self):
        return self.areasize_address

