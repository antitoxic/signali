from django.views.generic.base import View
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django.contrib.auth import login

from social.backends.email import EmailAuth
from restful.decorators import restful_view_templates
from restful.exception.verbose import VerboseHtmlOnlyRedirectException
from restful.http import HtmlOnlyRedirectSuccessDict

from notification import email
from security.views.password import PasswordResetAbstractView, PasswordResetConfirmAbstractView
from security.decorators import security_rule
from .forms import SignUpCheckpointForm, UserForm, UserFormNoPassword, ProfileUpdateForm

@restful_view_templates
class LoginView(View):
    def get(self, request):
        return {}


@restful_view_templates
class SignUpView(View):
    def get(self, request):
        return {}




@restful_view_templates
class SignUpCheckpointView(View):
    def get(self, request):
        details = request.session['partial_pipeline']['kwargs']['details']
        uid = request.session['partial_pipeline']['kwargs']['uid']
        return {
            'details': details,
            'uid': uid,
            'usecase': request.params.get('usecase', 'now'),
        }

    def post(self, request):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('user:signup-checkpoint')
        try:
            form = SignUpCheckpointForm(data=request.params)
            if form.is_valid():
                data = form.cleaned_data
                request.session['saved_email'] = data['email']
                request.session['saved_name'] = data['fullname']
                backend = request.session['partial_pipeline']['backend']
                return redirect('security:complete', backend=backend)
            else:
                raise failure.set_errors(form.errors)
        except Exception as e:
            raise failure.add_error('generic', str(e))



@restful_view_templates
class PasswordResetView(PasswordResetAbstractView):
    def get(self, request):
        return {}

    def post(self, request):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('user:password-reset')
        user, url = self.get_user_and_reset_url(request, 'user:password-reset-confirm', failure)
        try:
            email.send('user/password_reset_email', user.email, request=request, user=user, url=url)
        except:
            raise failure.add_error('generic', 'Could not email reset link')
        return HtmlOnlyRedirectSuccessDict({
            "email": user.email
        }).set_redirect('user:password-reset-sent')



@restful_view_templates
class PasswordResetSentView(View):
    def get(self, request):
        return {}



@restful_view_templates
class PasswordResetConfirmView(PasswordResetConfirmAbstractView):
    def get(self, request, uidb64=None, token=None):
        return {}

    def post(self, request, uidb64=None, token=None):
        failure = VerboseHtmlOnlyRedirectException()
        failure.set_redirect('user:password-reset-confirm', uidb64=uidb64, token=token)
        self.reset_password(request, uidb64, token, failure)
        return redirect('user:password-reset-complete')


@restful_view_templates
class PasswordResetCompleteView(View):
    def get(self, request):
        return {}


@restful_view_templates
class ProfileView(View):

    def extract_permission_target(self, request, pk):
        return self._get_user(request, pk)

    def _get_user(self, request, pk):
        UserModel = get_user_model()
        user = UserModel.objects.get(pk=pk)
        return user

    @security_rule('user.profile_view')
    def get(self, request, pk):
        return {
            'user': self._get_user(request, pk)
        }

    @security_rule('user.profile_change')
    def post(self, request, pk):
        failure = VerboseHtmlOnlyRedirectException().set_redirect('user:profile', pk=pk)
        user = self._get_user(request, pk)
        form = ProfileUpdateForm(request.params)
        if not form.is_valid():
            raise failure.set_errors(form.errors)

        UserUpdateForm = UserForm if 'password' in form.cleaned_data else UserFormNoPassword
        form = UserUpdateForm(instance=user, data=form.cleaned_data)
        if not form.is_valid():
            raise failure.set_errors(form.errors)

        try:
            user = form.save()
            if isinstance(form, UserForm):
                backend = EmailAuth()
                user.backend = '{}.{}'.format(backend.__module__, backend.__class__.__name__)
                login(request, user)
        except:
            failure.add_error('Problems with the database')

        return HtmlOnlyRedirectSuccessDict({
            "result": _("Successfully updated profile")
        }).set_redirect('user:profile', pk=pk)
