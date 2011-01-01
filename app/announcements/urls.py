from django.conf.urls.defaults import *

urlpatterns = patterns('app.announcements.views',
                       url(r'^$', 'overview'),
                       url(r'^deleted/$', 'overview_deleted'),
                       url(r'^add/$', 'add'),
                       url(r'^edit/(\d+)/?$', 'edit'),
                       url(r'^view/(\d+)/?$', 'view'),
                       url(r'^recover/(\d+)/?$', 'recover'),
                       url(r'^delete/(\d+)/?$', 'delete'),
                       url(r'^delete/(\d+)$', 'delete'),
                       )