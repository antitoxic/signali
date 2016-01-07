from django.db import models
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey
from mptt.managers import TreeManager


class AreaManager(TreeManager):
    def count_size(self, include=None, exclude=None):
        if exclude is not None:
            return self.exclude(size__in=[exclude]).count()
        else:
            return self.filter(size__in=[include]).count()


class BaseArea(MPTTModel):
    objects = AreaManager()

    class Meta:
        abstract = True
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    regulation_code = models.CharField(_('regulation code'), max_length=20, blank=True, null=True)
    regulation_codename = models.CharField(_('regulation codename'), max_length=20, blank=True, null=True)
    regulation_type = models.CharField(_('regulation type'), max_length=20, blank=True, null=True)
    title = models.CharField(_('title'), max_length=250, blank=False)
    parent = TreeForeignKey('self', related_name="children", verbose_name=_('parent area'), blank=True, null=True, db_index=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    def __str__(self):
        repr = self.title
        if self.is_root_node():
            return repr
        if self.regulation_type:
            repr = '{} {}'.format(self.regulation_type, repr)
        elif self.size.abbr:
            repr = '{} {}'.format(self.size.abbr, repr)
        else:
            repr = '{} ({})'.format(repr, self.size.title)
        if self.parent and not self.parent.is_root_node():
            repr = '{} — {}'.format(repr, self.parent.title)

        return repr

class BaseAreaSize(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('area size')
        verbose_name_plural = _('area sizes')

    title = models.CharField(_('title'), max_length=250, blank=False)
    abbr = models.CharField(_('abbreviation'), max_length=250, blank=True)

    def __str__(self):
        return self.title
