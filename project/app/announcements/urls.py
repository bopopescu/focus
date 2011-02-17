from django.conf.urls.defaults import *

urlpatterns = patterns('app.announcements.views',
                       url(r'^$', 'overview'),
                       url(r'^trashed/$', 'overview_trashed'),
                       url(r'^add/$', 'add'),
                       url(r'^edit/(\d+)/?$', 'edit'),
                       url(r'^view/(\d+)/?$', 'view'),
                       url(r'^recover/(\d+)/?$', 'recover'),
                       url(r'^trash/(\d+)/?$', 'trash'),
                       )