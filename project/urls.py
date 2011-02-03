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
                       (r'^hourregistrations/', include('app.hourregistrations.urls')),
                       (r'^typeOfWorks/addPop/?$', 'app.hourregistrations.views.addTypeOfWork'),
                       (r'^announcements/', include('app.announcements.urls')),
                       #settings for admin
                       (r'^admin/', include('app.admin.urls')),

                       (r'^profile/$', 'app.admin.views.profile.edit'),

                       #Stock
                       (r'^stock/products/', include('app.stock.products.urls')),
                       (r'^stock/productgroups/', include('app.stock.productgroups.urls')),
                       (r'^stock/currencies/', include('app.stock.currencies.urls')),
                       (r'^stock/productunits/', include('app.stock.productUnits.urls')),
                       #Suppliers
                       (r'^suppliers/', include('app.suppliers.urls')),
                       (r'^tickets/', include('app.tickets.urls')),
                       #Directlink for use of popup
                       #For adding users
                       #(r'participants/addPop/$', 'app.admin.users.views.addPop'),
                       #(r'users/addPop/$', 'app.admin.users.views.addPop'),

                       (r'testtest$', 'app.mail.views.overview'),


                       #Grant permissions
                       (
                       r'grant/role/(?P<role>\w+)/(?P<userorgroup>\w+)/(?P<user_id>\w+)/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\w+)/$'
                       , 'core.views.grant_role'),
                       (
                       r'grant/permission/(?P<perm>\w+)/(?P<userorgroup>\w+)/(?P<user_id>\w+)/(?P<app>\w+)/(?P<model>\w+)/(?P<object_id>\w+)/$'
                       , 'core.views.grant_permission'),

                       (r'testing', 'core.views.testing'),


                       #for adding currency
                       (r'unitForSizes/addPop/$', 'app.stock.productUnits.views.addPop'),
                       (r'priceVals/addPop/$', 'app.stock.currencies.views.addPop'),
                       (r'productGroups/addPop/$', 'app.stock.productgroups.views.addPop'),
                       )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()