# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('app.stock.products.views',
                       url(r'^$', 'overview'),
                       url(r'^add/$', 'add'),
                       url(r'^trashed/$', 'overview_trashed'),
                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/recover/?$', 'recover'),
                       url(r'^(?P<id>\d+)/view//?$', 'view'),
                       url(r'^(?P<id>\d+)/delete/?$', 'delete'),
                       url(r'^(?P<id>\d+)/addfile/?$', 'addFile'),
                       url(r'^(?P<id>\d+)/deletefile/(?P<fileID>\d+)?$', 'deleteFile'),
                       )