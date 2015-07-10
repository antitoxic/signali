import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models import Avg


class Rating(models.Model):
    criteria = models.CharField(_('criteria'), max_length=250, blank=False)
    added_at = models.DateTimeField(_('added at'), default=timezone.now)

    @property
    def score(self):
        return self.votes.all().aggregate(score=Avg('price')).score


class Vote(models.Model):
    rating = models.ForeignKey('Rating', related_name="votes", verbose_name=_("rating"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="votes", verbose_name=_("voter"))
    score = models.PositiveIntegerField(_('score'), max_length=250, blank=False)
    added_at = models.DateTimeField(_('added at'), default=timezone.now)

