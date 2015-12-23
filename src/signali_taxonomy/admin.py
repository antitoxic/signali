from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from taxonomy.admin import BaseCategoryAdmin, BaseKeywordAdmin
from signali_accessibility.forms import VisibilityColoredStyleFormMixin
from .models import Category, Keyword


class CategoryForm(forms.ModelForm, VisibilityColoredStyleFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = Category.objects.root_categories()

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryForm
    search_fields = ('title',)
    suit_form_tabs = (
        ('basic', _('basic')),
        ('visibility', _('visibility')),
    )
    list_display = ('title', 'is_featured', 'is_public',)
    list_editable = ('is_featured', 'is_public', )
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('title', 'parent', 'is_public')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-visibility',),
            'fields': ('is_featured', 'popularity', 'views', 'style')
        }),
    )


class KeywordForm(forms.ModelForm, VisibilityColoredStyleFormMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].label = _('keyword')

class KeywordAdmin(BaseKeywordAdmin):
    form = KeywordForm
    search_fields = ('title',)
    suit_form_tabs = (
        ('basic', _('basic')),
        ('visibility', _('visibility')),
    )
    fieldsets = (
        (None, {
            'classes': ('suit-tab suit-tab-basic',),
            'fields': ('title', 'is_public')
        }),
        (None, {
            'classes': ('suit-tab suit-tab-visibility',),
            'fields': ('is_featured', 'popularity', 'views', 'style')
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)
