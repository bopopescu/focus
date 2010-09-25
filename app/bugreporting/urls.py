from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('app.bugreporting.views',
    # Example:
    # (r'^iceonweb/', include('iceonweb.foo.urls')),
        url(r'^$', 'overview'), 
        url(r'^add/$', 'add'), 
        url(r'^view/(\d+)/?$',   'view'),
        url(r'^edit/(\d+)/?$', 'edit'), 
        url(r'^changeStatus/(\d+)/?',   'changeStatus'),
        url(r'^delete/(\d+)/?$', 'delete'), 
                
     # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)