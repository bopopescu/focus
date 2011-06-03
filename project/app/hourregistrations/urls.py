from django.conf.urls.defaults import *

urlpatterns = patterns('app.hourregistrations.views',
                       url(r'^$', 'calendar_today'),
                       url(r'^calendar/form/$', 'form'),
                       url(r'^calendar/employees/$', 'list_all_employees'),
                       url(r'^calendar/date_valid_for_edit/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
                           'date_valid_for_edit'),
                       url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/$', 'calendar_json'),
                       url(r'^calendar/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'calendar_day_json'),

                       #Archive
                       url(r'^archive/$', 'your_archive'),
                       url(r'^archive/(?P<user_id>\d+)$', 'user_archive'),
                       url(r'^archive/(?P<year>\d+)/(?P<month>\d+)/$', 'view_archived_month'),
                       url(r'^(?P<user_id>\d+)/archive/(?P<year>\d+)/(?P<month>\d+)/$', 'view_archived_month'),
                       url(r'^(?P<user_id>\d+)/archive/(?P<year>\d+)/(?P<month>\d+)/(?P<print_friendly>\d+)$', 'view_archived_month'),
                       )