from django.conf import settings
from .models import Setting

def public_settings(request):
    try:
        extra_context = {}
        for s in settings.PUBLIC_SETTINGS:
            extra_context[s] = getattr(settings, s)
        return extra_context
    except:
        return {}


def site_settings(request):
    try:
        return {"site": Setting.objects.all()[:1].get()}
    except:
        return {}