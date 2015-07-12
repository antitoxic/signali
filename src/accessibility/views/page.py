from django.views.generic.base import View
from restful.decorators import restful_view_templates
from django.shortcuts import get_object_or_404
from ..models import Page


@restful_view_templates
class PageView(View):
    def get(self, request, slug):
        return {
            "page": get_object_or_404(Page, slug=slug, is_public=True),
        }
