from django.views.generic.base import View
from restful.decorators import restful_view_templates
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from social.apps.django_app.utils import psa

from ..signals import post_email_validation

UserModel = get_user_model()


@restful_view_templates
class EmailValidationView(View):
    @method_decorator(psa())
    def get(self, request, backend):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('home')
        strategy = request.backend.strategy
        try:
            code = strategy.storage.code.get_code(request.params['verification_code'])
            user = UserModel.objects.get(email=code.email)
            user.is_email_validated = True
            user.save()
            code.delete()
            post_email_validation.send(UserModel, user=user)
            return HtmlOnlyRedirectSuccessDict({
                "email": request.user.email,
            }).set_redirect('home')
        except:
            raise failure.add_error('email_validation', _("This activation link is invalid"))

    @method_decorator(login_required)
    @method_decorator(psa())
    def post(self, request, backend):
        request.backend.strategy.send_email_validation(request.backend, request.user.email)
        return HtmlOnlyRedirectSuccessDict({
            "email": request.user.email,
        }).set_redirect('home')


@restful_view_templates
class EmailValidationSentView(View):
    def get(self, request):
        return {
            'email': request.session.get('email_validation_address')
        }

