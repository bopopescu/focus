from django.conf.urls.defaults import *

urlpatterns = patterns('app.tickets.views',
                       url(r'^assigned/$', 'assigned_to_user'),
                       url(r'^overview/$', 'overview'),
                       url(r'^assigned/(?P<id>\d+)/$', 'assigned_to_user'),
                       url(r'^trashed/$', 'overview_trashed'),
                       url(r'^new/?$', 'add'),
                       url(r'^(?P<id>\d+)/edit/$', 'edit'),
                       url(r'^(?P<id>\d+)/view/$', 'view'),
                       url(r'^(?P<id>\d+)/trash/$', 'trash'),
                       )