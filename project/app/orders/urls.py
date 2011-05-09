from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',
                       #ORDER
                       url(r'^order/$', 'order.overview'),
                       url(r'^order/my$', 'order.my_orders'),
                       url(r'^order/(?P<id>\d+)/view/$', 'order.view'),
                       url(r'^order/new/$', 'order.add'),
                       url(r'^order/(?P<id>\d+)/edit/$', 'order.edit'),
                       url(r'^order/(?P<id>\d+)/invoice/$', 'order.create_invoice'),
                       )