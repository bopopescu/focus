from django.conf.urls.defaults import *

urlpatterns = patterns('app.offers.views',
                       #OFFER
                       url(r'^$', 'overview'),
                       url(r'^new/$', 'add'),
                       url(r'^(?P<id>\d+)/edit/$', 'edit'),
                       url(r'^(?P<id>\d+)/view/$', 'view'),
                       url(r'^(?P<id>\d+)/history/?$', 'history'),
                       url(r'^(?P<id>\d+)/order/$', 'create_order'),
                       url(r'^(?P<id>\d+)/client/$', 'client_management'),
                       )