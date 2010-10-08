from django.conf.urls.defaults import *


urlpatterns = patterns('app.admin.views',
                
                
        #USERS       
        url(r'^$',                  'users.overview'), 
        url(r'^add/$',              'users.add'), 
        url(r'^edit/(\d+)/?$',      'users.edit'), 
        url(r'^view/(\d+)/?$',      'users.view'), 
        url(r'^delete/(\d+)/?$',    'users.delete'),
        
        #MEMBERSHIPS
        
        url(r'^memberships/$',              'memberships.overview'), 
        url(r'^addMembership/$',            'memberships.add'), 
        url(r'^editMembership/(\d+)/?$',    'memberships.edit'), 
        url(r'^viewMembership/(\d+)/?$',    'memberships.view'), 
        url(r'^deleteMembership/(\d+)/?$',  'memberships.delete'),
    
)
