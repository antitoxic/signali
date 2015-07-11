from django.contrib import admin
from .models import ContactPoint, Organisation, ContactPointRating
from location.models import Area
from adminextra.reverseadmin import ReverseModelAdmin
from django.forms import ModelForm

class ContactPointAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

class AddressForm(ModelForm):
    class Meta:
        model = Area
        fields = ('title', 'parent')

    def save(self, commit=True):
        from .apps import setting
        self.instance.size = setting('contact_address_areasize')
        return super().save(commit)


class OrganisationAdmin(ReverseModelAdmin):
    inline_type = 'tabular'
    inline_reverse = (('address', AddressForm),)

admin.site.register(ContactPoint, ContactPointAdmin)
admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(ContactPointRating)