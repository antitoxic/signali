from restful.decorators import restful_view_templates
from restful.pages import RestfulPaging
from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from security.decorators import security_rule

from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from .forms import get_contactpoint_from
from .apps import setting
from .signals import post_submit

ContactPointModel = setting('CONTACT_POINT_MODEL')
UserCriteriaFormClass = setting('CONTACT_USER_CRITERIA_FORM')


@restful_view_templates
class SingleView(View):
    def _get(self, slug):
        try:
            return ContactPointModel.objects.get_by_slug(slug)
        except ContactPointModel.DoesNotExist:
            raise Http404()

    def get(self, request, slug):
        return {
            "point": self._get(slug)
        }


@restful_view_templates
class ListView(View):
    form = None

    def get(self, request):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point-list')
        prefix = request.params.get('prefix', '')
        form = UserCriteriaFormClass(data=request.params, prefix=prefix)

        if not form.is_valid():
            raise failure.add_error(prefix+'form', form.errors)

        sorting = form.get_sorting()
        start = form.get_start()
        limit = form.get_limit()
        score, filters = form.to_search_expressions()
        points = ContactPointModel.objects.apply_criteria(score, filters, sorting)
        total = points.count()
        try:
            pages = RestfulPaging(total, form.get_start(), form.get_limit())
        except:
            pages = None
        return {
             "sorting": sorting,
             "form": form,
             "pages": pages,
             "points": points[start:(start+limit)],
             "total": total,
             "limit": limit,
        }

    @security_rule('contact.contactpoint_create')
    def post(self, request):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point-list')
        formname = request.params.get('prefix', '')+'form'
        form = self._get_form(request)

        if not form.is_valid():
            raise failure.add_error(formname, form.errors)

        try:
            instance = form.save()
            post_submit.send(instance.__class__, contactpoint=instance)
            return HtmlOnlyRedirectSuccessDict({
                "result": _("Successfully gave feedback")
            }).set_redirect('contact-point-list')
        except Exception as e:
            raise failure.add_error('generic', str(e))

    def _get_form(self, request):
        if self.form:
            return self.form
        self.form = get_contactpoint_from(request.params, prefix=request.params.get('prefix', None))
        self.form.is_valid() # no other way to trigger conversion of values to python objects
        return self.form

    def extract_permission_target(self, request):
        form = self._get_form(request)
        return form.instance
