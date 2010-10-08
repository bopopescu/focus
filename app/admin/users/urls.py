from django.conf.urls.defaults import *

urlpatterns = patterns('app.admin.users.views',      
        url(r'^$',                  'overview'), 
        url(r'^add/$',              'add'), 
        url(r'^edit/(\d+)/?$',      'edit'), 
        url(r'^view/(\d+)/?$',      'view'), 
        url(r'^delete/(\d+)/?$',    'delete'),
)