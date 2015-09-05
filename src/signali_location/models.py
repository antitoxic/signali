from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import BaseArea, BaseAreaSize, AreaManager
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin
from contact.apps import setting


class SignalAreaManager(AreaManager, VisibilityManagerMixin):
    def non_address(self):
        return self.exclude(size__in=[setting('contact_address_areasize')])

class Area(BaseArea, SignalVisibilityMixin):
    objects = SignalAreaManager()
    size = models.ForeignKey('AreaSize', related_name="areas", verbose_name=_("size"), blank=True, null=True)

class AreaSize(BaseAreaSize, SignalVisibilityMixin):
    pass


