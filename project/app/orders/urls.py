from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',


                       url(r'^$', 'overview'),
                       url(r'^invoice/$', 'overview_invoice'),
                       url(r'^archive/$', 'overview_archive'),
                       url(r'^offers/$', 'overview_offers'),

                       url(r'^add/$', 'add'),
                       url(r'^add_offer/$', 'add_offer'),

                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'view'),
                       url(r'^(?P<id>\d+)/history/?$', 'history'),

                       url(r'^(?P<id>\d+)/products/$', 'products'),
                       url(r'^(?P<id>\d+)/deleteorderline/(?P<orderlineID>\d+)$', 'delete_order_line'),

                       url(r'^(?P<id>\d+)/change_status/$', 'change_status'),

                       #TASKS
                       url(r'^(?P<id>\d+)/add_task/$', 'add_task'),
                       url(r'^(?P<id>\d+)/change_status_task/$', 'change_status_task'),

                       )