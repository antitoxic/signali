# home = ('', 'help.intro')
# guide = ('/guide/<name>', 'help.guide.page')
# #  view guide
# guide = ('/calendar', 'events.calendar') #restful
# # big calendar with all event, spannig 3 weeks behind and 3 weeks forwad
# guide = ('/calendar/event', 'events.event') #restful
# # get info, create new , update
# guide = ('/project/<name>', 'collaboration.projectdashboard') #restful
# # short info about project with link to more, collaboration area
# guide = ('/dashboard', 'collaboration.userdashboard') #non-restful
# # curretn tasks, current projects, dates, events joined....
# guide = ('/user/<username>', 'network.userprofile') #restful
# # project involved in, times asked, skillset...
# guide = ('/organisation/<name>', 'network.userprofile') #restful
# # displayed projects involved, users in organisation, donations,
from django.conf.urls import patterns, include, url
from siteguide.views.intro import IntroView
from django.conf import settings

from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', IntroView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
