import datetime

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _


class Rating(models.Model):
    criteria = models.CharField(_('criteria'), max_length=250, blank=False)
    score = models.PositiveIntegerField(_('score'), blank=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    added_at = models.DateTimeField(_('added at'), default=timezone.now)


class Vote(models.Model):
    score = models.PositiveIntegerField(_('score'), max_length=250, blank=False)
    rating = models.ForeignKey('Rating', related_name="votes", verbose_name=_("rating"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="votes", verbose_name=_("voter"))

