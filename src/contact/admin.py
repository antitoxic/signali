from django.contrib import admin

class BaseContactPointAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}