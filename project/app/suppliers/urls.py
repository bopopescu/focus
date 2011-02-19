from django.conf.urls.defaults import *

urlpatterns = patterns('app.suppliers.views',

                       url(r'^$', 'overview'),
                       url(r'^trashed$', 'overview_trashed'),
                       url(r'^add/$', 'add'),
                       url(r'^(?P<id>\d+)/edit/$', 'edit'),
                       url(r'^(?P<id>\d+)/view/$', 'view'),
                       url(r'^(?P<id>\d+)/history/$', 'history'),
                       url(r'^(?P<id>\d+)/delete/$', 'delete'),
                       )