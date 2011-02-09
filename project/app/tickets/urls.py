from django.conf.urls.defaults import *

urlpatterns = patterns('app.tickets.views',
                       url(r'^$', 'overview'),
                       url(r'^new/?$', 'add'),
                       )