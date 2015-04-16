from django.contrib import admin
from singlemodeladmin import SingleModelAdmin
from .models import Setting

class SettingAdmin(SingleModelAdmin):
    pass

admin.site.register(Setting, SettingAdmin)