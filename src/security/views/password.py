from django.views.generic.base import View
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.core.urlresolvers import reverse

from ..forms import SetPasswordForm, PasswordResetForm

class PasswordResetAbstractView(View):
    def get(self, request):
        raise NotImplementedError()

    @method_decorator(never_cache)
    def post(self, request):
        raise NotImplementedError()

    def get_user_and_reset_url(self, request, routename, failure):
        form = PasswordResetForm(request.params)
        if not form.is_valid():
            raise failure.set_errors(form.errors)

        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email__iexact=form.cleaned_data['email'])
        except:
            raise failure.add_error('generic', _('No user registered with this email'))

        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        url = request.build_absolute_uri(
            reverse(routename, kwargs={'uidb64': uidb64, 'token': token})
        )
        return user, url


class PasswordResetConfirmAbstractView(View):
    def _get_user(self, uidb64, token):
        UserModel = get_user_model()
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel.objects.get(pk=uid)
        assert uidb64 is not None and token is not None
        assert default_token_generator.check_token(user, token)
        return user

    def reset_password(self, request, uidb64, token, failure):
        try:
            user = self._get_user(uidb64, token)
        except:
            raise failure.add_error('generic', 'Invalid reset password link')

        form = SetPasswordForm(request.params)
        if not form.is_valid():
            raise failure.set_errors(form.errors)

        try:
            user.set_password(form.cleaned_data['new_password1'])
            user.save()
        except Exception as e:
            raise failure.add_error('generic', str(e))

    @method_decorator(never_cache)
    def get(self, request, uidb64=None, token=None):
        raise NotImplementedError()

    @method_decorator(sensitive_post_parameters())
    def post(self, request, uidb64=None, token=None):
        raise NotImplementedError()
