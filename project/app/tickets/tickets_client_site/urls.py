from django.conf.urls.defaults import *

urlpatterns = patterns('app.tickets.tickets_client_site.views',
                       url(r'^$', 'overview', name='client_overview'),
                       url(r'^view/(?P<id>\d+)/$', 'view', name='client_view'),
                       url(r'^login/$', 'login', name='client_login')
                       )