from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^signup/$', SignUpView.as_view(), name='signup'),
    url(r'^signup/checkpoint/$', SignUpCheckpointView.as_view(), name='signup-checkpoint'),
    url(r'^join/$', LoginView.as_view(), name='join'),
    url(r'^password/reset$', PasswordResetView.as_view(), name='password-reset'),
    url(r'^password/reset/sent$', PasswordResetSentView.as_view(), name='password-reset-sent'),
    url(r'^password/reset/success$', PasswordResetCompleteView.as_view(), name='password-reset-complete'),
)
