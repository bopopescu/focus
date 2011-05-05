from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',
                       #ORDER
                       url(r'^order/$', 'order.overview'),
                       url(r'^order/(?P<id>\d+)/view/$', 'order.view'),

                       #OFFER
                       url(r'^offer/$', 'offer.overview'),
                       url(r'^offer/new/$', 'offer.add'),
                       url(r'^offer/(?P<id>\d+)/edit/$', 'offer.edit'),
                       url(r'^offer/(?P<id>\d+)/view/$', 'offer.view'),
                       url(r'^offer/(?P<id>\d+)/order/$', 'offer.create_order'),
                       url(r'^offer/(?P<id>\d+)/client/$', 'offer.client_management'),
                       )