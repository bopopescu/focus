from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',


                       url(r'^$', 'overview'),
                       url(r'^invoice/$', 'overviewReadyForInvoice'),
                       url(r'^archive/$', 'overviewArchive'),
                       url(r'^offers/$', 'overviewOffers'),

                       url(r'^add/$', 'add'),
                       url(r'^addOffer/$', 'addOffer'),
                       url(r'^addPop/?$', 'addPop'),

                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'view'),
                       url(r'^(?P<id>\d+)/delete/$', 'delete'),

                       url(r'^(?P<id>\d+)/products/$', 'products'),
                       url(r'^(?P<id>\d+)/deleteorderline/(?P<orderlineID>\d+)$', 'deleteOrderLine'),

                       url(r'^(?P<id>\d+)/changeStatus/$', 'changeStatus'),

                       #TASKS
                       url(r'^(?P<id>\d+)/addTask/$', 'addTask'),
                       url(r'^(?P<id>\d+)/changeStatusTask/$', 'changeStatusTask'),

                       )