from django.db import models
from django.utils.translation import ugettext_lazy as _


class Keyword(models.Model):
    title = models.CharField(_('title'), max_length=250, blank=False)
    style = models.CharField(_('style'), max_length=250, blank=False)


class Category(models.Model):
    title = models.CharField(_('title'), max_length=250, blank=False)