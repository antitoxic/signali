from django.views.generic.base import View
from django.shortcuts import get_object_or_404
from django.apps import apps as django_apps
from django.conf import settings

from restful.decorators import restful_view_templates

PageModel = django_apps.get_model(settings.ACCESSIBILITY_PAGE_MODEL)

@restful_view_templates
class PageView(View):
    def get(self, request, slug):
        return {
            "page": get_object_or_404(PageModel, slug=slug, is_public=True),
        }
