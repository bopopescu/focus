from django.conf.urls.defaults import *

urlpatterns = patterns('app.files.folders.views',

        url(r'^add/(\d+)?/?$', 'add'),
        url(r'^edit/(\d+)/?$', 'edit'),
        url(r'^view/(\d+)/?$', 'view'),
        url(r'^delete/(\d+)$', 'delete'),
)