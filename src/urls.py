from django.conf.urls import patterns, include, url
from accessibility.views.intro import IntroView
from accessibility.views.page import PageView
from contact import views as contactpoint
from contact_feedback.views import ListView as FeedbackListView
from signali_notification.views import SubscriberListView
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', IntroView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^security/', include('security.urls', namespace='security')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^contact-points/$', contactpoint.ListView.as_view(), name='contact-point-list'),
    url(r'^contact-points/(?P<slug>[^/]+)/$', contactpoint.SingleView.as_view(), name='contact-point'),
    url(r'^contact-points/(?P<slug>[^/]+)/comments/$', FeedbackListView.as_view(), name='contact-point-feedback-list'),
    url(r'^contact-points/(?P<slug>[^/]+)/subscribers/$', SubscriberListView.as_view(), name='contact-point-subscriber-list'),
    url(r'^/(?P<slug>[^/]+)$', PageView.as_view(), name='page'),
    url(r'^redactor/', include('redactor.urls')),
)
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
