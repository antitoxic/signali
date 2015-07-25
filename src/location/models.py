from django.db import models
from django.utils.translation import ugettext_lazy as _


class AreaManager(models.Manager):
    def count_size(self, include=None, exclude=None):
        if exclude is not None:
            return self.exclude(size__in=[exclude]).count()
        else:
            return self.filter(size__in=[include]).count()

class Area(models.Model):
    objects = AreaManager()

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    title = models.CharField(_('title'), max_length=250, blank=False)
    parent = models.ForeignKey('self', related_name="children", verbose_name=_('parent area'), blank=True, null=True)
    size = models.ForeignKey('AreaSize', related_name="areas", verbose_name=_("size"), blank=True, null=True)

    def __str__(self):
        return '{} ({})'.format(self.title, self.size)

class AreaSize(models.Model):
    class Meta:
        verbose_name = _('area size')
        verbose_name_plural = _('area sizes')

    title = models.CharField(_('title'), max_length=250, blank=False)

    def __str__(self):
        return self.title
