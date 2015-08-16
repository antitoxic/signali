from django.db import models
from django.utils.translation import ugettext_lazy as _

from location.models import BaseArea, BaseAreaSize, AreaManager
from accessibility.models import VisibilityManagerMixin
from signali_accessibility.models import SignalVisibilityMixin


class SignalAreaManager(AreaManager, VisibilityManagerMixin):
    pass

class Area(BaseArea, SignalVisibilityMixin):
    objects = SignalAreaManager()
    size = models.ForeignKey('AreaSize', related_name="areas", verbose_name=_("size"), blank=True, null=True)

class AreaSize(BaseAreaSize, SignalVisibilityMixin):
    pass


