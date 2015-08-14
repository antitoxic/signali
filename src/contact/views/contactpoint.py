from django.views.generic.base import View
from restful.decorators import restful_view_templates
from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from django.shortcuts import get_object_or_404
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ..models import ContactPoint
from ..forms import UserCriteriaForm
from ..apps import setting


@restful_view_templates
class SingleView(View):
    def post(self, request, slug):
        contact_point = get_object_or_404(ContactPoint, slug=slug, visibility__is_public=True)
        return {
            'contact_point': contact_point
        }

    def get(self, request, slug):
        return {
            "contact_point": get_object_or_404(ContactPoint, slug=slug, visibility__is_public=True)
        }


@restful_view_templates
class CreateView(View):
    def get(self, request):
        return {}


@restful_view_templates
class ListView(View):
    def get(self, request):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point-list')
        UserCriteriaFormClass = setting('CONTACT_USER_CRITERIA_FORM', UserCriteriaForm)
        form = UserCriteriaFormClass(data=request.params)

        if not form.is_valid():
            raise failure.add_error('form', form.errors)

        points = ContactPoint.objects.apply_criteria(form.to_filters(), form.get_sorting())
        return {
             "points": points[form.get_start():form.get_limit()]
        }

    def post(self, request):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point-create')
        form = CreationForm(data=request.params)

        if form.is_valid():
            return HtmlOnlyRedirectSuccessDict({
                "result": _("Successfully created a new contact point")
            }).set_redirect('contact-point-list')
        else:
            raise failure.add_error('form', form.errors)


class CreationForm(ModelForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = ContactPoint
        fields = ['title', 'description', ]