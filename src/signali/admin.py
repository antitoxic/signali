from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Setting, Visibility
from accessibility.models import Page
from django import forms
from taxonomy.admin import CategoryAdmin
from location.admin import Area
from contact.admin import ContactPointAdmin


class SettingAdmin(SingleModelAdmin):
    pass


class VisibilityForm(forms.ModelForm):
    class Meta:
        model = Visibility
        fields = ('is_public', 'is_featured', 'style')


class AreaVisibilityForm(VisibilityForm):
    STYLE_CHOICES = (
        ('purple', 'Purple'),
        ('green', 'Green'),
        ('yellow', 'Yellow'),
        ('blue', 'Blue'),
        ('red', 'Red'),
    )
    style = forms.ChoiceField(choices=STYLE_CHOICES)


class VisibilityInline(admin.StackedInline):
    seamless = True
    form = VisibilityForm
    model = Visibility
    extra = 1
    max_num = 1

class AreaVisibilityInline(VisibilityInline):
    form = AreaVisibilityForm


class PageAdmin(admin.ModelAdmin):
    inlines = [VisibilityInline]

class PageAdmin(admin.ModelAdmin):
    inlines = [VisibilityInline]


CategoryAdmin.inlines = CategoryAdmin.inlines + [VisibilityInline]
ContactPointAdmin.inlines = ContactPointAdmin.inlines + [VisibilityInline]

class AreaAdmin(admin.ModelAdmin):
    inlines = [AreaVisibilityInline]

admin.site.unregister(Area)
admin.site.register(Area, AreaAdmin)


admin.site.register(Page, PageAdmin)
admin.site.register(Setting, SettingAdmin)
