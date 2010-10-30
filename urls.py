from django.conf.urls.defaults import *
from django.contrib import admin
import os
import settings

admin.autodiscover()

urlpatterns = patterns('',
                       
    ('^adminO/',                    include(admin.site.urls)),

    (r'^$',                         include('app.dashboard.urls')),
    
    (r'^dashboard/',                include('app.dashboard.urls')),
    
    (r'^customers/',                include('app.customers.urls')),
    
    (r'^contacts/',                 include('app.contacts.urls')),
    
    (r'^projects/',                 include('app.projects.urls')),           

    (r'^accounts/',                 include('app.accounts.urls')),

    (r'^files/',                    include('app.files.files.urls')),

    (r'^folders/',                  include('app.files.folders.urls')),

    (r'^orders/',                   include('app.orders.urls')),


    (r'^timetracking/',             include('app.timetracking.urls')),

    (r'^typeOfWorks/addPop/?$',     'app.timetracking.views.addTypeOfWork'),
    
    (r'^announcements/',            include('app.announcements.urls')),

    #settings for admin
    (r'^useradmin/',                include('app.admin.users.urls')),
    (r'^groupadmin/',               include('app.admin.memberships.urls')),


    #Stock
    (r'^stock/products/',           include('app.stock.products.urls')),
    (r'^stock/productgroups/',      include('app.stock.productgroups.urls')),
    (r'^stock/currencies/',         include('app.stock.currencies.urls')),
    (r'^stock/productunits/',       include('app.stock.productUnits.urls')),


    #Suppliers
    (r'^suppliers/',                include('app.suppliers.urls')),


    #Directlink for use of popup
        #For adding users
        (r'participants/addPop/$',      'app.admin.users.views.addPop'),
        (r'users/addPop/$',             'app.admin.users.views.addPop'),

        #for adding currency
        (r'unitForSizes/addPop/$',     'app.stock.productUnits.views.addPop'),
        (r'priceVals/addPop/$',        'app.stock.currencies.views.addPop'),
        (r'productGroups/addPop/$',     'app.stock.productgroups.views.addPop'),

 
    #media
    (r'^media/(?P<path>.*)', 'django.views.static.serve', {'document_root': os.path.join(settings.BASE_PATH, 'media')}),
   
    (r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
    
)