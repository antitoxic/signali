from django.contrib import admin
from .models import Category, Keyword

class CategoryAdmin(admin.ModelAdmin):
    pass

class KeywordAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Keyword, KeywordAdmin)