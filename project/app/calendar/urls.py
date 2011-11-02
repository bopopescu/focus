from django.conf.urls.defaults import *

urlpatterns = patterns('app.calendar.views',
                       url(r'^$', 'overview'),
                       url(r'^(?P<year>\d+)/(?P<month>\d+)/$', 'overview'),
                       url(r'^new/$', 'add'),
                       url(r'^(\d+)/edit/$', 'edit'),
                       url(r'^(\d+)/delete/', 'delete'),

                       url(r'^event_type/new/$', 'event_type_add'),
                       url(r'^event_type/new_ajax/$', 'add_event_type_ajax'),
                       url(r'^event_type/(\d+)/edit$', 'event_type_edit')

                       ,
                      )