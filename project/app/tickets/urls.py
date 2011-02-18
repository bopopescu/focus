from django.conf.urls.defaults import *

urlpatterns = patterns('app.tickets.views',
                       url(r'^$', 'overview'),
                       url(r'^trashed/$', 'overview_trashed'),
                       url(r'^new/?$', 'add'),
                       url(r'^(?P<id>\d+)/edit/$', 'edit'),
                       url(r'^(?P<id>\d+)/view/$', 'view'),
                       url(r'^(?P<id>\d+)/trash/$', 'trash'),
                       )