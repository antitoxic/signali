from django.utils.translation import ugettext_lazy as _

from accessibility.models import BasePage, VisibilityMixin
from sorl.thumbnail import ImageField
from signali.uploads import Uploader


class SignalVisibilityMixin(VisibilityMixin):
    class Meta:
        abstract = True
    preview = ImageField(verbose_name=_("preview"), null=True, blank=True, upload_to=Uploader('visibility'))
    cover = ImageField(verbose_name=_("cover"), null=True, blank=True, upload_to=Uploader('visibility'))

class Page(BasePage, SignalVisibilityMixin):
    pass
