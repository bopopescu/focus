from django.conf.urls.defaults import *

urlpatterns = patterns('app.email.views',

                       url(r'parse/?$', 'parse'),

                       )