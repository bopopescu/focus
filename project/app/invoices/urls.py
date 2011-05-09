from django.conf.urls.defaults import *

urlpatterns = patterns('app.invoices.views',
                       #OFFER
                       url(r'^$', 'overview'),
                       url(r'^(?P<id>\d+)/view/$', 'view'),
                       url(r'^(?P<id>\d+)/edit/$', 'edit'),
                       url(r'^new/$', 'add'),
                       )