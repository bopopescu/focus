from django.conf.urls.defaults import *

urlpatterns = patterns('app.customers.views',

                       url(r'^$', 'overview'),

                       url(r'^deleted/?$', 'overview_deleted'),
                       url(r'^all/?$', 'overview_all'),

                       url(r'^add/?$', 'add'),
                       url(r'^addPop/?$', 'addPop'),

                       url(r'^edit/(\d+)/?$', 'edit'),
                       url(r'^view/(\d+)/?$', 'view'),

                       url(r'^permissions/(\d+)/?$', 'permissions'),
                       url(r'^delete/(\d+)/?$', 'delete'),

                       url(r'^recover/(\d+)/?$', 'recover'),


                       )