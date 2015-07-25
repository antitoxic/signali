from django.db import models
from django.utils.translation import ugettext_lazy as _


class Keyword(models.Model):
    class Meta:
        verbose_name = _('keyword')
        verbose_name_plural = _('keywords')
    title = models.CharField(_('title'), max_length=250, blank=False)
    style = models.CharField(_('style'), max_length=250, blank=False)

    def __str__(self):
        return self.title



class CategoryManager(models.Manager):
    def root_categories_plus_children(self):
        return self.filter(parent__isnull=True).prefetch_related('children')

class Category(models.Model):
    objects = CategoryManager()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    parent = models.ForeignKey('self', verbose_name=_('parent category'), related_name='children', blank=True, null=True)
    title = models.CharField(_('title'), max_length=250, blank=False)

    def __str__(self):
        if self.parent is None:
            return self.title
        return '{} ({})'.format(self.title, self.parent)