from django.views.generic.base import View
from restful.decorators import restful_view_templates


@restful_view_templates
class IntroView(View):
    def get(self, request):
        return {
            "test": ":)",
        }
