from django.conf.urls.defaults import *

urlpatterns = patterns('app.timetracking.views',

                       url(r'^$', 'overview'),
                       url(r'^add/$', 'add'),
                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/delete/?$', 'delete'),
                       url(r'^calendar/', 'calendar'),

                       #Ajax

                       url(r'^ajaxEditCalendar/$', 'ajaxEditCalendar'),

                       )