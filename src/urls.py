from django.conf.urls import patterns, include, url
from accessibility.views.intro import IntroView
from accessibility.views.page import PageView
from contact.views import contactpoint
from contact_feedback.views import ListView as FeedbackListView
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', IntroView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^security/', include('security.urls', namespace='security')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^contact-points/$', contactpoint.ListView.as_view(), name='contact-point-list'),
    url(r'^contact-points/new/$', contactpoint.CreateView.as_view(), name='contact-point-create'),
    url(r'^contact-points/(?P<slug>[^/]+)/$', contactpoint.SingleView.as_view(), name='contact-point'),
    url(r'^contact-points/(?P<slug>[^/]+)/comments/$', FeedbackListView.as_view(), name='contact-point-feedback-list'),
    url(r'^/(?P<slug>[^/]+)$', PageView.as_view(), name='page'),
)
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
