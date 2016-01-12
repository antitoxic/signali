from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField
from accessibility.models import VisibilityMixin, VisibilityManagerMixin

from .uploads import Uploader



class Setting(models.Model):
    class Meta:
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

    title = models.CharField(_('title'), max_length=250, blank=False)
    title_short = models.CharField(_('short title'), max_length=250, blank=False, default="")
    description = models.CharField(_('description'), max_length=250, blank=False)
    google_analytics = models.CharField(_('google analytics account id'), max_length=250, blank=False)
    areasize_address = models.ForeignKey('signali_location.AreaSize',
                                         verbose_name=_('Which size denotes address-level area'),
                                         blank=False)
    cover = ImageField(verbose_name=_("cover"), null=True, blank=True, upload_to=Uploader('signali'))
    facebook_share = ImageField(verbose_name=_("facebook share image"), null=True, blank=True, upload_to=Uploader('signali'))

    @property
    def contact_address_areasize(self):
        return self.areasize_address

    @property
    def cover_url(self):
        return self.cover.url

    @classmethod
    def main(cls):
        return cls.objects.all()[:1].get()


class PartnerManager(models.Manager, VisibilityManagerMixin):
    pass


class Partner(VisibilityMixin):
    objects = PartnerManager()

    class Meta:
        verbose_name = _('partner')
        ordering = ['order']
        verbose_name_plural = _('partners')

    order = models.PositiveIntegerField()
    title = models.CharField(_('title'), max_length=250, blank=False)
    url = models.URLField(_('url'), max_length=250, blank=False)
    provides = models.CharField(_('provides'), max_length=250, blank=True)
    logo = ImageField(verbose_name=_("logo"), null=True, blank=True, upload_to=Uploader('signali'))


