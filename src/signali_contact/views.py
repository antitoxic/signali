from django.views.generic.base import View

from restful.decorators import restful_view_templates
import watson

from .models import ContactPoint


@restful_view_templates
class SearchView(View):
    form = None

    def get(self, request):
        search = request.params.get('query')
        return {
            "results": watson.search(search, models=(ContactPoint,))
        }
