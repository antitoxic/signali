from functools import wraps

from django.utils.decorators import available_attrs
from django.utils.translation import ugettext_lazy as _

from restful.exception.htmlonlyredirect import PermissionDeniedHtmlOnlyRedirectException

from .views.mixin import SecuredViewMixin
from .utils import get_permission_denied_login_url

def security_rule(rulename):
    def decorator(action):
        # maintain correct stacktrace name and doc
        @wraps(action, assigned=available_attrs(action))
        def _checkrule(view, request, *args, **kwargs):
            failure = PermissionDeniedHtmlOnlyRedirectException(_('No permission to access page'))
            failure.set_redirect(get_permission_denied_login_url(request))

            if not isinstance(view, SecuredViewMixin):
                raise Exception(_("Can't secure view. Must inherit SecuredViewMixin mixin"))
            rule_args = view.extract_permission_args(request, *args, **kwargs)
            if not request.user.has_perm(rulename, *rule_args):
                raise failure
            return action(view, request, *args, **kwargs)

        return _checkrule

    return decorator