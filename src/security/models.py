from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Limit(models.Model):
    action = models.CharField(_('action name'), max_length=255, db_index=True)
    count = models.PositiveIntegerField(_('visits'), default=0)
    last_executed_timestamp = models.PositiveIntegerField(_('unix timestamp of last successful action execution'), null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="rate_limits", verbose_name=_("user"), null=True)
    ip = models.GenericIPAddressField(_("ip address"), null=True)

