from django.views.generic.base import View
from restful.decorators import restful_view_templates
from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from django.shortcuts import get_object_or_404
from django import forms
from django.forms import ModelForm

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
        return {
             "points": ContactPoint.objects.filter(**criteria)[int(criteria['start']):int(criteria['limit'])]
        }

    def post(self, request):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('contact-point-create')
        raise failure.add_error('what', 'bat')
        form = CreationForm(data=request.params)
        status = 200

        if form.is_valid:
            pass
        else:
            status = 400

        return {
            'status': 'success'
        }, status


class CreationForm(ModelForm):
    # email = forms.EmailField(required=True)

    class Meta:
        model = ContactPoint
        fields = ['title', 'description', ]