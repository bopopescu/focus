from django.conf.urls.defaults import *

urlpatterns = patterns('app.admin.memberships.views',      
        url(r'^$',                  'overview'), 
        url(r'^new/$',              'add'),
        url(r'^edit/(\d+)/?$',      'edit'), 
        url(r'^view/(\d+)/?$',      'view'), 
        url(r'^delete/(\d+)/?$',    'delete'),
)