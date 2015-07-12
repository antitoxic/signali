from django.views.generic.base import View
from restful.decorators import restful_view_templates
from restful.shortcuts import errors, success


@restful_view_templates
class IntroView(View):
    def get(self, request):
        return {
            "test": ":)",
            "errors": errors(request),
            "success": success(request),
        }
