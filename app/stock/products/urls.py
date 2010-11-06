from django.conf.urls.defaults import *

urlpatterns = patterns('app.stock.products.views',
        url(r'^$', 'overview'),
        url(r'^add/$', 'add'),
        url(r'^deleted/$', 'overview_deleted'),
        url(r'^edit/(\d+)/?$', 'edit'),
        url(r'^recover/(\d+)/?$', 'recover'),
        url(r'^view/(\d+)/?$', 'view'),
        url(r'^delete/(\d+)/?$', 'delete'),
)