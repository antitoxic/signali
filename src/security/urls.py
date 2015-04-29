from django.conf.urls import patterns, url
from .views import entry

urlpatterns = patterns('',
    url(r'^login/(?P<backend>[^/]+)/$', entry.CredentialsView.as_view(),
        name='begin'),
    url(r'^token/(?P<backend>[^/]+)/', entry.TokenView.as_view(),
        name='token'),
    url(r'^complete/(?P<backend>[^/]+)/$', entry.RegisterView.as_view(),
        name='complete'),
    url(r'^email-validation/$', entry.ValidationSentView.as_view(),
        name='email-validation'),
    url(r'^logout/$', entry.LogoutView.as_view(),
        name='logout'),
)
