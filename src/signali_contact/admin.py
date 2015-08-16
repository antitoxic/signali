from django.contrib import admin
from django.forms import ModelForm

from sorl.thumbnail.admin import AdminImageMixin
from adminextra.reverseadmin import ReverseModelAdmin

from contact.admin import BaseContactPointAdmin
from signali_location.models import Area
from .models import ContactPoint, Organisation

class ContactPointAdmin(BaseContactPointAdmin, AdminImageMixin):
    pass


class AddressForm(ModelForm):
    class Meta:
        model = Area
        fields = ('title', 'parent')

    def save(self, commit=True):
        from signali.utils import setting
        self.instance.size = setting('contact_address_areasize')
        return super().save(commit)


class OrganisationPointAdmin(ReverseModelAdmin):
    inline_type = 'tabular'
    inline_reverse = (('address', AddressForm),)


admin.site.register(ContactPoint, ContactPointAdmin)
admin.site.register(Organisation, OrganisationPointAdmin)