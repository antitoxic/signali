from restful.decorators import restful_view_templates
from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException

from django.views.generic.base import View
from django.utils.translation import ugettext as _
from django.http import Http404

from security.decorators import security_rule
from .forms import get_feedbackfrom
from .apps import setting
from .signals import post_submit


@restful_view_templates
class ListView(View):
    contactpoint = None
    form = None

    @security_rule('contact.feedback_create')
    def post(self, request, slug):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point', slug=slug)
        formname = request.params.get('prefix', '')+'form'
        form = self._get_form(request, self._get_contactpoint(slug))

        if not form.is_valid():
            raise failure.add_error(formname, form.errors)

        try:
            instance = form.save()
            post_submit.send(instance.__class__, feedback=instance)
            return HtmlOnlyRedirectSuccessDict({
                "result": _("Successfully gave feedback")
            }).set_redirect('contact-point', slug=slug)
        except Exception as e:
            raise failure.add_error('generic', str(e))

    def extract_permission_target(self, request, slug):
        form = self._get_form(request, self._get_contactpoint(slug))
        return form.instance

    def _get_form(self, request, contactpoint):
        if self.form:
            return self.form
        self.form = get_feedbackfrom(contactpoint, request.params, prefix=request.params.get('prefix', None))
        self.form.is_valid() # no other way to trigger conversion of values to python objects
        return self.form

    def _get_contactpoint(self, slug):
        if self.contactpoint:
            return self.contactpoint

        ContactPointModel = setting('CONTACT_POINT_MODEL')
        try:
            self.contactpoint = ContactPointModel.objects.get_by_slug(slug)
        except ContactPointModel.DoesNotExist:
            raise Http404()

        return self.contactpoint
