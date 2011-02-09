from django.conf.urls.defaults import *

urlpatterns = patterns('app.customers.views',

                       url(r'^$', 'overview'),

                       url(r'^deleted/?$', 'overview_trashed'),
                       url(r'^all/?$', 'overview_all'),

                       url(r'^add/?$', 'add'),
                       url(r'^add_ajax/?$', 'add_ajax'),

                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'view'),
                       url(r'^(?P<id>\d+)/trash/?$', 'trash'),
                       url(r'^(?P<id>\d+)/recover/?$', 'recover'),
                       )