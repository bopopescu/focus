# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('app.files.views',
                       url(r'^add/(\d+)?/?$', 'add_file'),
                       url(r'^edit/(\d+)/?$', 'edit_file'),
                       )