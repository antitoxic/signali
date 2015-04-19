from django.contrib import admin
from .models import ContactPoint, ContactPointRequirement, Orgаnisation

class ContactPointAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(ContactPoint, ContactPointAdmin)
admin.site.register(ContactPointRequirement)
admin.site.register(Orgаnisation)