from django.conf.urls.defaults import *

urlpatterns = patterns('app.company.views',
                        url(r'^$', 'overview'),
                        url(r'^new/$', 'add'),
                        url(r'^(?P<id>\d+)/edit/$', 'edit'),
                       )