from django.core.urlresolvers import reverse


def get_validation_url(strategy, backend, code):
    return strategy.build_absolute_uri(
        reverse('security:complete', args=(backend.name,))
    ) + '?verification_code=' + code.code
