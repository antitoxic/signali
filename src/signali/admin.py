from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Setting, Visibility
from accessibility.models import Page
from django.forms import ModelForm
from taxonomy.admin import CategoryAdmin


class SettingAdmin(SingleModelAdmin):
    pass


class VisibilityForm(ModelForm):
    class Meta:
        model = Visibility
        fields = ('is_featured', 'style')


class VisibilityInline(admin.StackedInline):
    seamless = True
    form = VisibilityForm
    model = Visibility
    extra = 1
    max_num = 1


class PageAdmin(admin.ModelAdmin):
    inlines = [VisibilityInline]


CategoryAdmin.inlines = CategoryAdmin.inlines + [VisibilityInline]

admin.site.register(Page, PageAdmin)
admin.site.register(Setting, SettingAdmin)
