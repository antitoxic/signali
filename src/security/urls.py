from django.conf.urls import patterns, url
from .views import entry

urlpatterns = patterns('',
    # show a page where the user allows authorization or a page with form where the user enters details
    url(r'^login/(?P<backend>[^/]+)/$', entry.CredentialsView.as_view(),
        name='begin'),
    # login and registration via token
    url(r'^token/(?P<backend>[^/]+)/', entry.TokenAuthView.as_view(),
        name='token'),
    # login and registration
    url(r'^complete/(?P<backend>[^/]+)/$', entry.AuthView.as_view(),
        name='complete'),
    url(r'^email-validation/$', entry.ValidationSentView.as_view(),
        name='email-validation'),
    url(r'^logout/$', entry.LogoutView.as_view(),
        name='logout'),
)
