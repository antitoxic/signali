from django.db import models
from django.utils.translation import ugettext_lazy as _


class BaseKeyword(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('keyword')
        verbose_name_plural = _('keywords')
    title = models.CharField(_('title'), max_length=250, blank=False)

    def __str__(self):
        return self.title

    def site_wide_pk(self):
        return 'taxonomy-keyword-'+str(self.pk)


class CategoryQuerySetMixin(object):
    def children(self):
        return self.exclude(parent=None)

    def roots(self):
        return self.filter(parent=None)

    def prefetch_children(self):
        return self.prefetch_related('children')

    def prefetch_parent(self):
        return self.select_related('parent')

    @property
    def pk_list(self):
        return list(self.values_list('id', flat=True))


class BaseCategory(models.Model):

    class Meta:
        abstract = True
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    parent = models.ForeignKey('self', verbose_name=_('parent category'), related_name='children', blank=True, null=True)
    title = models.CharField(_('title'), max_length=250, blank=False)

    def __str__(self):
        if self.parent is None:
            return self.title
        return '{}: {}'.format(self.parent.title, self.title)

    def site_wide_pk(self):
        return 'taxonomy-category-'+str(self.pk)

