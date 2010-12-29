from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',


                       url(r'^$', 'overview'),
                       url(r'^invoice/$', 'overviewReadyForInvoice'),
                       url(r'^archive/$', 'overviewArchive'),
                       url(r'^offers/$', 'overviewOffers'),

                       url(r'^add/$', 'add'),
                       url(r'^addOffer/$', 'addOffer'),
                       url(r'^addPop/?$', 'addPop'),

                       url(r'^edit/(\d+)/?$', 'edit'),
                       url(r'^view/(\d+)/?$', 'view'),
                       url(r'^delete/(\d+)$', 'delete'),

                       url(r'^changeStatus/(\d+)$', 'changeStatus'),

                       url(r'^permissions/(\d+)/?', 'permissions'),


                       #TASKS
                       url(r'^addTask/(\d+)$', 'addTask'),
                       url(r'^changeStatusTask/(\d+)$', 'changeStatusTask'),

                       )