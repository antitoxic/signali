from django import forms
from django.contrib import admin
from taxonomy.admin import BaseCategoryAdmin, BaseKeywordAdmin
from signali_accessibility.forms import VisibilityColoredStyleFormMixin

from .models import Category, Keyword


class CategoryForm(forms.ModelForm, VisibilityColoredStyleFormMixin):
    pass

class CategoryAdmin(BaseCategoryAdmin):
    form = CategoryForm


class KeywordForm(forms.ModelForm, VisibilityColoredStyleFormMixin):
    pass

class KeywordAdmin(BaseKeywordAdmin):
    form = KeywordForm


admin.site.register(Category, CategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)