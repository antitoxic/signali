from django.views.generic.base import View
from restful.decorators import restful_view_templates
from django.http.response import HttpResponseRedirectBase
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, get_user_model
from django.conf import settings

from restful.http import HtmlOnlyRedirectSuccessDict
from restful.exception.verbose import VerboseHtmlOnlyRedirectException, VerboseException
from social.backends.oauth import BaseOAuth1, BaseOAuth2
from social.apps.django_app.utils import psa
from social.apps.django_app.views import auth, complete, _do_login as login

from ..exceptions import WrongPasswordAuthException, AuthException, UserExistsAuthException, UserDoesNotExistAuthException

UserModel = get_user_model()

@restful_view_templates
class CredentialsView(View):
    def get(self, request, backend):
        return auth(request, backend)

    def post(self, request, backend):
        return self.get(request, backend)


def transform_auth_result(request, result):
    user = request.user
    redirect_url = settings.LOGIN_REDIRECT_URL
    status_code = 200
    if isinstance(result, UserModel):
        user = result
    elif isinstance(result, HttpResponseRedirectBase):
        redirect_url = result.url
        if user.is_new:
            status_code = 202
    return HtmlOnlyRedirectSuccessDict({
        "user": user,
        "backend": request.backend.name,
        "redirect": redirect_url,
    }).set_redirect(redirect_url), status_code


# to be mainly accessed by AJAX
@restful_view_templates
class TokenAuthView(View):
    @method_decorator(psa('security:complete'))
    def post(self, request, backend):
        failure = VerboseException()
        if isinstance(request.backend, BaseOAuth1):
            token = {
                'oauth_token': request.params.get('auth_token'),
                'oauth_token_secret': request.params.get('access_token_secret'),
            }
        elif isinstance(request.backend, BaseOAuth2):
            token = request.params.get('auth_token')
        else:
            raise failure.add_error('Wrong backend type')

        auth_result = request.backend.do_auth(
            access_token=token,
            user=request.user if request.user.is_authenticated() else None
        )
        result = transform_auth_result(request, auth_result)
        user = result[0]["user"]
        if user.is_active:
            login(request.backend, user, user.social_user)
        else:
            raise failure.add_error('Inactive user')

        return result


@restful_view_templates
class AuthView(View):
    def get(self, request, backend, *args, **kwargs):
        failure = VerboseHtmlOnlyRedirectException()
        failure_redirect = request.params.get('retry')
        if failure_redirect:
            failure.set_redirect(failure_redirect)
        else:
            failure.set_redirect('security:begin', backend=backend)

        try:
            auth_result = complete(request, backend, *args, **kwargs)
            return transform_auth_result(request, auth_result)
        except WrongPasswordAuthException as e:
            raise failure.by(e).add_error('password', str(e))
        except UserExistsAuthException as e:
            raise failure.by(e).add_error('email', str(e))
        except UserDoesNotExistAuthException as e:
            raise failure.by(e).add_error('email', str(e))
        except AuthException as e:
            raise failure.by(e).add_error('auth', str(e))
        except Exception as e:
            raise failure.by(e).add_error('auth', str(e))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
