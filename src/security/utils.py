from django.core.urlresolvers import reverse
from urllib.parse import urlparse, urlunparse, ParseResult
from django.conf import settings
from django.http import QueryDict
from django.contrib.auth import REDIRECT_FIELD_NAME


def get_validation_url(strategy, backend, code):
    return strategy.build_absolute_uri(
        reverse('security:email-validation', args=(backend.name,))
    ) + '?verification_code=' + code.code


def get_permission_denied_login_url(request):
    login_url = settings.LOGIN_URL
    current_url = request.get_full_path()
    login_url_parts = urlparse(login_url)
    login_url_querystring = QueryDict(login_url_parts.query, mutable=True)
    login_url_querystring[REDIRECT_FIELD_NAME] = current_url
    url = ParseResult(
        scheme=login_url_parts.scheme,
        netloc=login_url_parts.netloc,
        path=login_url_parts.path,
        params=login_url_parts.params,
        query=login_url_querystring.urlencode(safe='/'),
        fragment=login_url_parts.fragment
    )
    return urlunparse(url)
