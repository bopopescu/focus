from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('app.contacts.views',
    # Example:
    # (r'^iceonweb/', include('iceonweb.foo.urls')),
        url(r'^$', 'overview'), 

        url(r'^deleted/?$', 'overview_deleted'),
        url(r'^all/?$', 'overview_all'),

        url(r'^add/$', 'add'), 
        url(r'^addPop/$', 'addPop'), 
        url(r'^edit/(\d+)$', 'edit'), 
        url(r'^view/(\d+)$', 'view'),
        url(r'^permissions/(\d+)$', 'permissions'),
        url(r'^delete/(\d+)$', 'delete'), 
                
     # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)