from django.contrib import admin
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.admin import AdminImageMixin
from adminextra.reverseadmin import ReverseModelAdmin
from django_bootstrap_datetimepicker.widgets import BootstrapDateTimeInput

from contact.admin import BaseContactPointAdmin
from signali_location.models import Area
from .models import ContactPoint, Organisation

betterDateTimePicker = BootstrapDateTimeInput(format="%d.%m.%Y %H:%M")

extended_booelan_fields = [
    'is_multilingual',
    'is_response_guaranteed',
    'is_verifiable',
    'is_confirmation_issued',
    'is_mobile_friendly',
    'is_final_destination',
    'is_anonymous_allowed',
]


class ContactPointForm(forms.ModelForm):
    class Meta:
        model = ContactPoint
        exclude = []

    force_required = extended_booelan_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fieldname in self.fields:
            if fieldname in self.force_required:
                self.fields[fieldname].choices = ContactPoint.EXTENDED_BOOLEAN_CHOICES


class ContactPointAdmin(BaseContactPointAdmin, AdminImageMixin):
    form = ContactPointForm
    prepopulated_fields = {"slug": ("title",)}
    suit_form_tabs = (
        ('basic', _('basic')),
        ('visibility', _('visibility')),
        ('meta', _('meta')),
    )
    # formfield_overrides = {
    #     models.DateTimeField: {'widget': betterDateTimePicker},
    # }

    radio_fields = dict((field,admin.HORIZONTAL) for field in extended_booelan_fields)

    list_display = ('title', 'category')
    list_display_links = ('title',)
    search_fields = ('title', 'description',)

    fieldsets = (

        (None, {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('title', 'slug',)
        }),
        (_('key content'), {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('url', 'category', 'keywords', 'operational_area', 'organisation')
        }),
        (_('visuals'), {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('preview', 'cover')
        }),
        (_('text'), {
            'classes': ('suit-tab suit-tab-basic full-width',),
            'fields': ('description', 'notes',)
        }),
        (_('features'), {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': extended_booelan_fields
        }),
        (_('requirements'), {
            'classes': ('suit-tab suit-tab-basic full-width',),
            'fields': ((
                           'is_registration_required',
                           'is_photo_required',
                           'is_esign_required',
                           'is_name_required',
                           'is_email_required',
                           'is_pic_required',
                           'is_address_required',
                           'is_location_required',
                       ),)
        }),
        (None, {
            'classes': ('suit-tab suit-tab-visibility',),
            'fields': ('popularity', 'views', 'is_featured', 'is_public', 'style')
        }),
        # (None, {
        #     'classes': ('suit-tab suit-tab-meta',),
        #     'fields': ('created_at', 'changed_at',)
        # }),
    )


class AddressForm(forms.ModelForm):
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
