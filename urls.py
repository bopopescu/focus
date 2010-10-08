from django.conf.urls.defaults import *
from django.contrib import admin
import os
import settings

admin.autodiscover()

urlpatterns = patterns('',
                       
    ('^admin/',                     include(admin.site.urls)),

    (r'^$',                         include('app.dashboard.urls')),
    
    (r'^dashboard/',                include('app.dashboard.urls')),
    
    (r'^customers/',                include('app.customers.urls')),
    
    (r'^contacts/',                 include('app.contacts.urls')),
    
    (r'^projects/',                 include('app.projects.urls')),           

    (r'^accounts/',                 include('app.accounts.urls')),
    
    (r'^orders/',                   include('app.orders.urls')),
    
    (r'^timetracking/',             include('app.timetracking.urls')),
    (r'^typeOfWorks/addPop/?$',     'app.timetracking.views.addTypeOfWork'),
    
    (r'^announcements/',            include('app.announcements.urls')),
    
    (r'^bugreporting/',             include('app.bugreporting.urls')),
    
    
    #settings
    (r'^useradmin/',                include('app.admin.urls')),
    (r'^groupadmin/',                include('app.admin.urls')),
    
    
    #Directlink for use of popup
        #For adding users
        (r'participants/addPop/$',      'app.admin.views.users.addPop'),
        (r'users/addPop/$',             'app.admin.views.users.addPop'),
 
 
    #media
    (r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': os.path.join(settings.BASE_PATH, 'media')}),
   
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    
)