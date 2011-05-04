from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',

                        #ORDER
                       url(r'^$', 'order.overview'),
                       url(r'^invoice/$', 'order.overview_invoice'),
                       url(r'^archive/$', 'order.overview_archive'),
                       url(r'^offers/$', 'order.overview_offers'),

                       url(r'^add/$', 'order.add'),
                       url(r'^add_offer/$', 'order.add_offer'),

                       url(r'^(?P<id>\d+)/edit/?$', 'order.edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'order.view'),
                       url(r'^(?P<id>\d+)/history/?$', 'order.history'),

                       url(r'^(?P<id>\d+)/products/$', 'order.products'),
                       url(r'^(?P<id>\d+)/deleteorderline/(?P<orderlineID>\d+)$', 'order.delete_order_line'),

                       url(r'^(?P<id>\d+)/change_status/$', 'order.change_status'),

                       )