from django.db import models
from django.utils import timezone
from redactor.fields import RedactorField
from django.utils.translation import ugettext_lazy as _


class Page(models.Model):
    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('URL part'), max_length=255)
    contents = RedactorField(verbose_name=_('Content'))
    created_at = models.DateTimeField(_('Added at'), default=timezone.now)
    changed_at = models.DateTimeField(_('Added at'), default=timezone.now)
    is_public = models.BooleanField(_('Published'), default=False)


class AbstractVisibility(models.Model):
    class Meta:
        abstract = True
        verbose_name = _('visibility')
        verbose_name_plural = _('visibility options')
    popularity = models.PositiveIntegerField(_('popularity'), default=0)
    views = models.PositiveIntegerField(_('popularity'), default=0)
    is_featured = models.BooleanField(_('is featured'), default=False)
    is_public = models.BooleanField(_('is public'), default=False)
    style = models.CharField(blank=True, null=True, max_length=255, verbose_name=_('Style [technical]'))