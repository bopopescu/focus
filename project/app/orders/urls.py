from django.conf.urls.defaults import *

urlpatterns = patterns('app.orders.views',
                       #ORDER
                       url(r'^order/$', 'order.overview'),
                       url(r'^order/my$', 'order.my_orders'),
                       url(r'^order/new/$', 'order.add'),
                       url(r'^order/(?P<id>\d+)/view/$', 'order.view'),
                       url(r'^order/(?P<id>\d+)/edit/$', 'order.edit'),
                       url(r'^order/(?P<id>\d+)/history/?$', 'order.history'),
                       url(r'^order/(?P<id>\d+)/hourregistrations/$', 'order.view_hourregistrations'),
                       url(r'^order/(?P<id>\d+)/preview_html/$', 'order.preview_order_html'),
                       url(r'^order/(?P<id>\d+)/invoice/$', 'order.create_invoice'),

                       url(r'^order/(?P<id>\d+)/plan_work/$', 'order.plan_work'),
                       url(r'^order/(?P<id>\d+)/plan_work/(?P<year>\d+)/(?P<month>\d+)/$', 'order.plan_work'),

                       url(r'^order/(?P<id>\d+)/participants/((?P<permission_id>\d+)/)?$', 'order.participants'),
                       url(r'^order/(?P<id>\d+)/participants/(?P<permission_id>\d+)/delete/$', 'order.delete_permission_from_participants'),

                       #Files
                       url(r'^(?P<id>\d+)/files/$', 'files.overview'),
                       url(r'^(?P<id>\d+)/files/add/$', 'files.add_file'),
                       url(r'^(?P<id>\d+)/files/(?P<file_id>\d+)/edit/$', 'files.edit_file'),
                       )