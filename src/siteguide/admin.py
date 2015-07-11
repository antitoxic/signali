from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Setting, Visibility
from django.forms import ModelForm
from contact.admin import Organisation, OrganisationAdmin
from taxonomy.admin import Category, CategoryAdmin
admin.site.unregister(Organisation)

class SettingAdmin(SingleModelAdmin):
    pass

class VisibilityForm(ModelForm):
    class Meta:
        model = Visibility
        fields = ('is_featured',)

class VisibilityInline(admin.StackedInline):
    seamless = True
    form = VisibilityForm
    model = Visibility
    extra = 1
    max_num = 1

OrganisationAdmin.inlines = OrganisationAdmin.inlines + [VisibilityInline]
CategoryAdmin.inlines = CategoryAdmin.inlines + [VisibilityInline]

admin.site.register(Setting, SettingAdmin)
admin.site.register(Organisation, OrganisationAdmin)