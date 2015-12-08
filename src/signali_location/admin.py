from django.contrib import admin
from .models import Area, AreaSize
from django.utils.translation import ugettext_lazy as _


class AreaAdmin(admin.ModelAdmin):
    suit_form_tabs = (
        ('basic', _('basic')),
        ('visibility', _('visibility')),
    )
    list_display = ('title', 'size', 'parent')
    list_filter = (
        'size',
    )
    search_fields = ('title',)
    ordering = ('title',)
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('title', 'parent', 'size', 'is_public')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-visibility',),
            'fields': ('is_featured', 'popularity', 'views', 'style')
        }),
    )


admin.site.register(Area, AreaAdmin)
admin.site.register(AreaSize)

