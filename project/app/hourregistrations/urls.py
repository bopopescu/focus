from django.conf.urls.defaults import *

urlpatterns = patterns('app.hourregistrations.views',

                       url(r'^$', 'overview'),
                       url(r'^new/$', 'add'),
                       url(r'^archive/$', 'your_archive'),
                       url(r'^archive/(?P<user_id>\d+)$', 'user_archive'),
                       url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$', 'viewArchivedMonth'),
                       url(r'^(?P<user_id>\d+)/archive/(?P<year>\d+)/(?P<month>\d+)/$', 'viewArchivedMonth'),
                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/delete/?$', 'delete'),
                       url(r'^calendar/$', 'calendar_today'),
                       url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/(?P<week>\d+)/(?P<day>\d+)/', 'calendar'),

                       #Ajax
                       url(r'^ajaxEditCalendar/$', 'ajaxEditCalendar'),

                       url(r'^ajax/(?P<id>\d+)?$', 'ajax'),

                       )