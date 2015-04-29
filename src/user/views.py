from django.views.generic.base import View
from django.shortcuts import redirect

from restful.decorators import restful_view_templates
from restful.exception.verbose import VerboseHtmlOnlyRedirectException

from .forms import SignUpCheckpointForm
from notification import email
from security.views.password import PasswordResetAbstractView, PasswordResetConfirmAbstractView

@restful_view_templates
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return redirect('home')

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
                request.session['saved_name'] = data['name']
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
        user, url = self.get_user_and_reset_url(request, failure)
        try:
            email.send('user/password_reset_email', user.email, user=user, url=url)
        except:
            raise failure.add_error('generic', 'Could not email reset link')
        return redirect('user:password-reset-sent')



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