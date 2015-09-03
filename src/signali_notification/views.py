from restful.decorators import restful_view_templates
from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException

from django.views.generic.base import View
from django.utils.translation import ugettext as _
from django.http import Http404

from .forms import get_subscriber_form
from signali_contact.models import ContactPoint


@restful_view_templates
class SubscriberListView(View):

    def post(self, request, slug):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point', slug=slug)
        formname = request.params.get('prefix', '')+'form'

        try:
            contactpoint = ContactPoint.objects.get_by_slug(slug)
        except ContactPoint.DoesNotExist:
            raise Http404()

        form = get_subscriber_form(contactpoint, request.params, prefix=request.params.get('prefix', None))

        if not form.is_valid():
            raise failure.add_error(formname, form.errors)

        try:
            instance = form.save()
            return HtmlOnlyRedirectSuccessDict({
                "result": _("Successfully subscribed for contact point"),
                "subscription": instance
            }).set_redirect('contact-point', slug=slug)
        except Exception as e:
            raise failure.add_error('generic', str(e))
