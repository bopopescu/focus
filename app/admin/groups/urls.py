from django.conf.urls.defaults import *

urlpatterns = patterns('app.admin.groups.views',
        url(r'^$',                  'overview'), 
        url(r'^new/$',              'add'),
        url(r'^(?P<id>\d+)/edit/$',      'edit'),
        url(r'^(?P<id>\d+)/view/$',      'view'),
        url(r'^(?P<id>\d+)/delete/$',    'delete'),
)