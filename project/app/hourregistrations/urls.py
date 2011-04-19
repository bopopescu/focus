from django.conf.urls.defaults import *

urlpatterns = patterns('app.hourregistrations.views',
                           url(r'^$', 'calendar_today'),
                           url(r'^calendar/form/$', 'form'),
                           url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/$', 'calendar_json'),
                           url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'calendar_day_json'),
                       )