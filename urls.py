# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import os
import settings

urlpatterns = patterns('',
                       (r'^$', include('app.dashboard.urls')),
                       (r'^dashboard/', include('app.dashboard.urls')),
                       (r'^customers/', include('app.customers.urls')),
                       (r'^contacts/', include('app.contacts.urls')),
                       (r'^company/', include('app.company.urls')),
                       (r'^projects/', include('app.projects.urls')),
                       (r'^accounts/', include('app.accounts.urls')),
                       (r'^files/', include('app.files.files.urls')),
                       (r'^folders/', include('app.files.folders.urls')),
                       (r'^orders/', include('app.orders.urls')),
                       (r'^search/', include('app.search.urls')),
                       (r'^hourregistrationsOLD/', include('app.hourregistrations.urls')),
                       (r'^typeOfWorks/addPop/?$', 'app.hourregistrations.views.addTypeOfWork'),
                       (r'^announcements/', include('app.announcements.urls')),
                       #settings for admin
                       (r'^admin/users/', include('app.admin.users.urls')),
                       (r'^admin/groups/', include('app.admin.groups.urls')),
                       (r'^admin/company/', include('app.admin.company.urls')),
                       (r'^profile/$', 'app.admin.users.profile.edit'),
                       #Stock
                       (r'^stock/products/', include('app.stock.products.urls')),
                       (r'^stock/productgroups/', include('app.stock.productgroups.urls')),
                       (r'^stock/currencies/', include('app.stock.currencies.urls')),
                       (r'^stock/productunits/', include('app.stock.productUnits.urls')),
                       #Suppliers
                       (r'^suppliers/', include('app.suppliers.urls')),
                       #Directlink for use of popup
                       #For adding users
                       (r'participants/addPop/$', 'app.admin.users.views.addPop'),
                       (r'users/addPop/$', 'app.admin.users.views.addPop'),

                       #Grant permissions
                       (
                       r'grant/role/(?P<role>\w+)/(?P<userorgroup>\w+)/(?P<user_id>\w+)/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\w+)/$'
                       , 'core.views.grant_role'),
                       (
                       r'grant/permission/(?P<perm>\w+)/(?P<userorgroup>\w+)/(?P<user_id>\w+)/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\w+)/$'
                       , 'core.views.grant_permission'),

                       #for adding currency
                       (r'unitForSizes/addPop/$', 'app.stock.productUnits.views.addPop'),
                       (r'priceVals/addPop/$', 'app.stock.currencies.views.addPop'),
                       (r'productGroups/addPop/$', 'app.stock.productgroups.views.addPop'),
                       #media
                       (r'^media/(?P<path>.*)', 'django.views.static.serve',
                        {'document_root': os.path.join(settings.BASE_PATH, 'media')}),
                       #(r'^my_admin/jsi18n', 'django.views.i18n.javascript_catalog'),
                       )