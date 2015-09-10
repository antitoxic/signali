from django.utils.translation import ugettext_lazy as _

from accessibility.models import BasePage, VisibilityMixin
from sorl.thumbnail import ImageField
from signali.uploads import Uploader
from signali.models import Setting


class SignalVisibilityMixin(VisibilityMixin):
    class Meta:
        abstract = True
    preview = ImageField(verbose_name=_("preview"), null=True, blank=True, upload_to=Uploader('visibility'))
    cover = ImageField(verbose_name=_("cover"), null=True, blank=True, upload_to=Uploader('visibility'))

class Page(BasePage, SignalVisibilityMixin):
    def get_cover_img(self):
        if self.cover:
            return self.cover
        return Setting.main().cover
