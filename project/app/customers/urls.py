from django.conf.urls.defaults import *

urlpatterns = patterns('app.customers.views',

    url(r'^$', 'customer.overview'),

    url(r'^deleted/?$', 'customer.overview_trashed'),
    url(r'^all/?$', 'customer.overview_all'),

    url(r'^add/?$', 'customer.add'),
    url(r'^add_ajax/?$', 'customer.add_ajax'),

    url(r'^(?P<id>\d+)/edit/?$', 'customer.edit'),
    url(r'^(?P<id>\d+)/history/?$', 'customer.history'),
    url(r'^(?P<id>\d+)/view/?$', 'customer.view'),
    url(r'^(?P<id>\d+)/contacts/?$', 'customer.list_contacts'),
    url(r'^(?P<id>\d+)/contacts/remove/(?P<contact_id>\d+)$', 'customer.remove_contact_from_customer'),
    url(r'^(?P<id>\d+)/trash/?$', 'customer.trash'),
    url(r'^(?P<id>\d+)/restore/?$', 'customer.restore'),


    #Files
    url(r'^(?P<id>\d+)/files/$', 'files.overview'),
    url(r'^(?P<id>\d+)/files/add/$', 'files.add_file'),
    url(r'^(?P<id>\d+)/files/(?P<file_id>\d+)/edit/$', 'files.edit_file'),


)