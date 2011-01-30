# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('app.stock.currencies.views',
                       url(r'^$', 'overview'),
                       url(r'^add/$', 'add'),
                       url(r'^edit/(\d+)/?$', 'edit'),
                       url(r'^delete/(\d+)/?$', 'delete'),
                       )