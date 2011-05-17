from django.conf.urls.defaults import *

urlpatterns = patterns('app.tickets.views',
                       url(r'^overview/$', 'overview'),
                       url(r'^overview/(?P<status_id>\d+)/$', 'overview'),
                       url(r'^assigned/$', 'assigned_to_user'),
                       url(r'^assigned/(?P<status_id>\d+)/$', 'assigned_to_user'),
                       url(r'^assigned/(?P<id>\d+)/(?P<status_id>\d+)/$', 'assigned_to_user'),
                       url(r'^trashed/$', 'overview_trashed'),
                       url(r'^new/?$', 'add'),
                       url(r'^(?P<id>\d+)/edit/$', 'edit'),
                       url(r'^(?P<id>\d+)/view/$', 'view'),
                       url(r'^(?P<id>\d+)/trash/$', 'trash'),
                       url(r'^add_type_ajax/$', 'add_ticket_type_ajax'),
                       url(r'^(?P<id>\d+)/client/$', 'client_management'),
                       url(r'^visibility_update/$', 'ajax_change_update_visibility'),
                       )