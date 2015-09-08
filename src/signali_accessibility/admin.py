from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from django_bootstrap_datetimepicker.widgets import BootstrapDateTimeInput

from .models import Page

betterDateTimePicker = BootstrapDateTimeInput(format="%d.%m.%Y %H:%M")

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    suit_form_tabs = (
        ('basic', _('basic')),
        ('visibility', _('visibility')),
        ('meta', _('meta')),
    )
    # formfield_overrides = {
    #     models.DateTimeField: {'widget': betterDateTimePicker},
    # }

    list_display = ('title',)
    list_display_links = ('title', )
    search_fields = ('title', 'contents',)

    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('title', 'slug','is_public')
        }),
        (_('text'), {
            'classes': ('suit-tab suit-tab-basic full-width',),
            'fields': ('contents',)
        }),
        (_('visuals'), {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('preview', 'cover',)
        }),
        (None, {
            'classes': ('suit-tab suit-tab-visibility',),
            'fields': ('popularity', 'views', 'is_featured', 'style')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-meta',),
            'fields': ('created_at', 'changed_at',)
        }),
    )


admin.site.register(Page, PageAdmin)
