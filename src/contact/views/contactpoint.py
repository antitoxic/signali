from django.views.generic.base import View
from restful.decorators import restful_view_templates
from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from django.shortcuts import get_object_or_404
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _

from ..models import ContactPoint


@restful_view_templates
class SingleView(View):
    def post(self, request, slug):
        contact_point = get_object_or_404(ContactPoint, slug=slug, is_public=True)
        return {
            'contact_point': contact_point
        }

    def get(self, request, slug):
        return {
            "contact_point": get_object_or_404(ContactPoint, slug=slug, is_public=True)
        }


@restful_view_templates
class CreateView(View):
    def get(self, request):
        return {}


@restful_view_templates
class ListView(View):
    def get(self, request):
        criteria = {
            "start": 0,
            "limit": 20,
        }
        criteria.update(request.params)
        points = ContactPoint.objects.apply_criteria(criteria)

        return {
             "points": points[int(criteria['start']):int(criteria['limit'])]
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