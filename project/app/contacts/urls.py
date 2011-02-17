from django.conf.urls.defaults import *

urlpatterns = patterns('app.contacts.views',
                       url(r'^$', 'overview'),

                       url(r'^trashed/?$', 'overview_trashed'),
                       url(r'^all/?$', 'overview_all'),

                       url(r'^new/$', 'add'),
                       url(r'^add_ajax/$', 'add_ajax'),

                       url(r'^(?P<id>\d+)/edit$', 'edit'),
                       url(r'^(?P<id>\d+)/editimage$', 'editImage'),
                       url(r'^(?P<id>\d+)/history$', 'history'),
                       url(r'^(?P<id>\d+)/view$', 'view'),
                       url(r'^(?P<id>\d+)/delete$', 'trash'),
                       )
