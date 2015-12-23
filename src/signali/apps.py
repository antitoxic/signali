from functools import update_wrapper
from django.contrib.admin import sites
from django.shortcuts import redirect
from django.contrib.admin.apps import AdminConfig

original_get_url = sites.AdminSite.get_urls

def redirect_view(request):
    return redirect('admin:signali_contact_contactpointgrouped_changelist')

def admin_get_urls(self):
    from django.conf.urls import patterns, url
    def wrap(view, cacheable=False):
        def wrapper(*args, **kwargs):
            return self.admin_view(view, cacheable)(*args, **kwargs)
        return update_wrapper(wrapper, view)
    urlpatterns = original_get_url(self)
    urlpatterns.pop(0)
    return patterns('',
        url(r'^$', wrap(redirect_view), name='index'),
    ) + urlpatterns




class SignaliAdminConfig(AdminConfig):
    def ready(self):
        super().ready()
        self.module.autodiscover()
        sites.AdminSite.get_urls = admin_get_urls
        sites.site = sites.AdminSite()
