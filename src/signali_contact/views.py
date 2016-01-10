from django.views.generic.base import View
from django.utils import timezone

from restful.decorators import restful_view_templates
from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from watson import search as watson
from security.decorators import security_rule

from .models import ContactPoint
from .signals import post_visit
from contact.views import SingleView


@restful_view_templates
class SearchView(View):
    form = None

    def get(self, request):
        search = request.params.get('query')
        return {
            "results": watson.filter(ContactPoint.objects.children().public(), search)
        }


@restful_view_templates
class VisitsView(SingleView):
    form = None

    def extract_permission_target(self, request, slug):
        return request

    @security_rule('contact.visit')
    def post(self, request, slug):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point', slug=slug)
        point = self._get(slug)
        if request.user.is_authenticated():
            point.visits += 1
        else:
            point.anonymous_visits += 1

        point.last_visited_at = timezone.now()

        try:
            point.save()
            post_visit.send(point.__class__, contactpoint=point, user=request.user)
        except:
            raise failure.add_error('db', "Database issues")
