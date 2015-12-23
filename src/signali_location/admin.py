from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Area, AreaSize
from location.forms import AreaAutosuggestWidget
from signali_contact.models import ContactPoint


class AreaAdminForm(forms.ModelForm):
    class Meta:
        model = Area
        exclude = []
        widgets = {
            'parent': AreaAutosuggestWidget,
        }


class AreaAdmin(admin.ModelAdmin):
    form = AreaAdminForm
    suit_form_includes = (
        ('admin/area_contact_points.html', 'bottom', 'points'),
    )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context["related_points"] = ContactPoint.objects.filter(children__operational_area_id=object_id)
        return super().change_view(request, object_id, form_url, extra_context)

    suit_form_tabs = (
        ('basic', _('basic')),
        ('visibility', _('visibility')),
        ('legislative', _('legislative')),
        ('points', _('contact points')),
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
            'classes': ('suit-tab suit-tab-legislative',),
            'fields': ('regulation_code', 'regulation_codename', 'regulation_type')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-visibility',),
            'fields': ('is_featured', 'style')
        }),
    )


admin.site.register(Area, AreaAdmin)
admin.site.register(AreaSize)

