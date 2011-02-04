# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('app.projects.views',

                       url(r'^$', 'overview'),

                       url(r'^timeline/?$', 'timeline'),
                       
                       url(r'^deleted/?$', 'overview_deleted'),
                       url(r'^all/?$', 'overview_all'),

                       url(r'^add/$', 'add'),
                       url(r'^add_ajax/$', 'add_ajax'),

                       url(r'^(?P<id>\d+)/edit/?$', 'edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'view'),
                       url(r'^(?P<id>\d+)/delete/?$', 'delete'),
                    )