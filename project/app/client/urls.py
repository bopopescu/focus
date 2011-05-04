from django.conf.urls.defaults import *

urlpatterns = patterns('app.client.views',

                       url(r'^$', 'tickets.overview', name='tickets.client_overview'),


                       #Login
                       url(r'^login/$', 'login.login', name='login.client_login'),
                       url(r'^logout/$', 'login.logout', name='login.client_logout'),

                       #Tickets
                       url(r'^tickets/$', 'tickets.overview', name='tickets.client_overview'),
                       url(r'^tickets/view/(?P<id>\d+)/$', 'tickets.view', name='tickets.client_view'),

                       #Offers
                       url(r'^offers/$', 'offers.overview', name='offers.client_overview'),
                       url(r'^offers/view/(?P<id>\d+)/$', 'offers.view', name='offers.client_view'),

                       )