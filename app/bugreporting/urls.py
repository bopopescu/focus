from django.conf.urls.defaults import *

urlpatterns = patterns('app.bugreporting.views',

        url(r'^$',                      'overview'), 
        url(r'^add/$',                  'add'), 
        url(r'^view/(\d+)/?$',          'view'),
        url(r'^edit/(\d+)/?$',          'edit'), 
        url(r'^addComment/(\d+)/?$',    'addComment'),
        url(r'^changeStatus/(\d+)/?',   'changeStatus'),
        url(r'^delete/(\d+)/?$',        'delete'),                

)