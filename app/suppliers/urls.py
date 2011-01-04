from django.conf.urls.defaults import *

urlpatterns = patterns('app.suppliers.views',

        url(r'^$', 'overview'),
        url(r'^add/$', 'add'),
        url(r'^addPop/$', 'addPop'),
        url(r'^edit/(\d+)$', 'edit'),
        url(r'^delete/(\d+)$', 'delete'),
)