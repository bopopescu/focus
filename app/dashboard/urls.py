from django.conf.urls.defaults import *

urlpatterns = patterns('app.dashboard.views',

        url(r'^$', 'overview'),
        url(r'^logs/$', 'logs'),
        url(r'^notifications/$','notifications'),

)