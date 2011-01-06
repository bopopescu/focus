from django.conf.urls.defaults import *

import core.django_cron
core.django_cron.autodiscover()

urlpatterns = patterns('app.customers.views',

                       url(r'^$', 'overview'),

                       url(r'^deleted/?$', 'overview_deleted'),
                       url(r'^all/?$', 'overview_all'),

                       url(r'^add/?$', 'add'),
                       url(r'^addPop/?$', 'addPop'),

                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'view'),
                       url(r'^(?P<id>\d+)/delete/?$', 'delete'),
                       url(r'^(?P<id>\d+)/recover/?$', 'recover'),
                       )