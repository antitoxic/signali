from django.views.generic.base import View
from restful.decorators import restful_view_templates
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout


from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from social.apps.django_app.utils import psa
from social.apps.django_app.views import auth, complete, _do_login as login

from ..exceptions import WrongPasswordException, AuthException, UserExistsException


@restful_view_templates
class CredentialsView(View):
    def get(self, request, backend):
        return auth(request, backend)

    def post(self, request, backend):
        return self.get(request, backend)

# to be mainly accessed by AJAX
@restful_view_templates
class TokenView(View):

    @method_decorator(psa('security:complete'))
    def post(self, request, backend):
        auth_result = backend.do_auth(
            access_token=request.params.get('auth_token'),
            user=request.user.is_authenticated() and request.user or None
        )
        if request.is_ajax() and isinstance(auth_result, HttpResponseRedirectBase):
            return {
                "result": {
                    "redirect": auth_result.url,
                }
            }, 202
        else:
            login(backend, auth_result, auth_result.social_user)
            return {
                "result": {
                    "user": {
                        "first_name": auth_result.first_name,
                        "last_name": auth_result.last_name,
                        "username": auth_result.username,
                        "pk": auth_result.pk,
                       }
                }
            }


@restful_view_templates
class RegisterView(View):
    def get(self, request, backend, *args, **kwargs):
        failure = VerboseHtmlOnlyRedirectException()
        failure_redirect = request.params.get('retry')
        if failure_redirect:
            failure.set_redirect(failure_redirect)
        else:
            failure.set_redirect('security:begin', backend=backend)

        try:
            return complete(request, backend, *args, **kwargs)
        except WrongPasswordException as e:
            raise failure.add_error('password', str(e))
        except UserExistsException as e:
            raise failure.add_error('email', str(e))
        except AuthException as e:
            raise failure.add_error('auth', str(e))


    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


@restful_view_templates
class ValidationSentView(View):
    def get(self, request):
        return {
             'email': request.session.get('email_validation_address')
        }