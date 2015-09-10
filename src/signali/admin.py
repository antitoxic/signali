from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from singlemodeladmin import SingleModelAdmin
from suit.admin import SortableModelAdmin

from .models import Setting, Partner


class SettingAdmin(SingleModelAdmin):
    pass


class PartnerAdmin(SortableModelAdmin):
    list_display = ('title', 'url',  'is_featured', 'is_public',)
    list_editable = ('is_featured', 'is_public', )
    list_display_links = ('title',)
    search_fields = ('title', 'url',)

    fieldsets = (

        (None, {
            'fields': ('title', 'url',  'logo',  'is_public', 'is_featured', )
        }),
        (_('text'), {
            'fields': ('provides',)
        })
    )


admin.site.register(Setting, SettingAdmin)
admin.site.register(Partner, PartnerAdmin)
