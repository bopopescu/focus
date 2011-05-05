from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',
                       #ORDER
                       url(r'^order/$', 'order.overview'),

                       #OFFER
                       url(r'^offer/$', 'offer.overview'),
                       url(r'^offer/new/$', 'offer.add'),
                       url(r'^offer/(?P<id>\d+)/edit/$', 'offer.edit'),
                       url(r'^offer/(?P<id>\d+)/view/$', 'offer.view'),
                       url(r'^offer/(?P<id>\d+)/client/$', 'offer.client_management'),
                       )