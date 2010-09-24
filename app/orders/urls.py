from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',
        url(r'^$', 'overview'), 

        url(r'^add/$', 'add'), 
        url(r'^addPop/?$', 'addPop'),

        url(r'^edit/(\d+)/?$', 'edit'), 
        url(r'^view/(\d+)/?$', 'view'),
        url(r'^delete/(\d+)$', 'delete'), 

        url(r'^permissions/(\d+)/?', 'permissions'),

)