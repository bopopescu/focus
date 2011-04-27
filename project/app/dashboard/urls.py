# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('app.dashboard.views',
                           url(r'^$', 'overview'),
                           url(r'^notifications/$', 'notifications'),
                      )