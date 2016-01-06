from django.views.generic.base import View

import watson
from restful.decorators import restful_view_templates

from signali_location.models import Area


@restful_view_templates
class SearchView(View):

    def get(self, request):
        search = request.params.get('query')
        print(search)
        return {
            "results": watson.search(search, models=(Area.objects.non_address(),))
        }
