from django.db import models
from django.utils.translation import ugettext_lazy as _
from accessibility.models import AbstractVisibility
from taxonomy.models import Category, CategoryManager


class Setting(models.Model):
    class Meta:
        verbose_name = _('setting')
        verbose_name_plural = _('settings')

    title = models.CharField(_('title'), max_length=250, blank=False)
    description = models.CharField(_('description'), max_length=250, blank=False)
    google_analytics = models.CharField(_('google analytics account id'), max_length=250, blank=False)
    areasize_address = models.ForeignKey('location.AreaSize',
                                         verbose_name=_('Which size denotes address-level area'),
                                         blank=False)

    @property
    def contact_address_areasize(self):
        return self.areasize_address


class Visibility(AbstractVisibility):
    page = models.OneToOneField('accessibility.Page', related_name="visibility", verbose_name=_("page"), blank=True,
                                null=True)
    category = models.OneToOneField('taxonomy.Category', related_name="visibility", verbose_name=_("category"),
                                    blank=True, null=True)
    contactpoint = models.OneToOneField('contact.ContactPoint', related_name="visibility",
                                        verbose_name=_("contact point"), blank=True, null=True)
    area = models.OneToOneField('location.Area', related_name="visibility", verbose_name=_("area"), blank=True,
                                null=True)


class CategoryManagerProxy(CategoryManager):
    def popular(self):
        return self\
                   .all()\
                   .extra(select={'is_featured': Visibility._meta.db_table + '.is_featured OR NULL'})\
                   .order_by('visibility__popularity', 'is_featured')


class CategoryProxy(Category):
    objects = CategoryManagerProxy()

    class Meta:
        proxy = True
