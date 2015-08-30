from django.views.generic.base import View
from restful.decorators import restful_view_templates
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, get_user_model

from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException, VerboseException
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.apps.django_app.utils import psa
from social.apps.django_app.views import auth, complete, _do_login as login

from ..exceptions import WrongPasswordAuthException, AuthException, UserExistsAuthException, UserDoesNotExistAuthException

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
        failure = VerboseException()
        if isinstance(request.backend, BaseOAuth1):
            token = {
                'oauth_token': request.params.get('auth_token'),
                'oauth_token_secret': request.params.get('access_token_secret'),
            }
        elif isinstance(request.backend, BaseOAuth2):
            token = request.params.get('auth_token'),
        else:
            raise failure.add_error('Wrong backend type')

        auth_result = backend.do_auth(
            access_token=token,
            user=request.user if request.user.is_authenticated() else None
        )
        if isinstance(auth_result, HttpResponseRedirectBase):
            return HtmlOnlyRedirectSuccessDict({
                "result": {
                    "redirect": auth_result.url
                }
            }).set_redirect(auth_result.url), 202
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
        except WrongPasswordAuthException as e:
            raise failure.by(e).add_error('password', str(e))
        except UserExistsAuthException as e:
            raise failure.by(e).add_error('email', str(e))
        except UserDoesNotExistAuthException as e:
            raise failure.by(e).add_error('email', str(e))
        except AuthException as e:
            raise failure.by(e).add_error('auth', str(e))

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
