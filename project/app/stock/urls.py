# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('app.stock.views',
                       #Product
                       url(r'^product/$', 'product.overview'),
                       url(r'^product/add/$', 'product.add'),
                       url(r'^product/trashed/$', 'product.overview_trashed'),
                       url(r'^product/(?P<id>\d+)/edit/?$', 'product.edit'),
                       url(r'^product/(?P<id>\d+)/recover/?$', 'product.recover'),
                       url(r'^product/(?P<id>\d+)/view//?$', 'product.view'),
                       url(r'^product/(?P<id>\d+)/delete/?$', 'product.delete'),
                       url(r'^product/(?P<id>\d+)/addfile/?$', 'product.addFile'),
                       url(r'^product/(?P<id>\d+)/deletefile/(?P<fileID>\d+)?$', 'product.deleteFile'),
                       url(r'^ajax/product/$', 'product.autocomplete'),

                       #Units
                       url(r'^unit/$', 'productunit.overview'),
                       url(r'^unit/add/$', 'productunit.add'),
                       url(r'^unit/add_ajax/$', 'productunit.add_ajax'),
                       url(r'^unit/(?P<id>\d+)/edit/$', 'productunit.edit'),
                       url(r'^unit/(?P<id>\d+)/delete/$', 'productunit.delete'),

                       #Product group
                       url(r'^productgroup/$', 'productgroup.overview'),
                       url(r'^productgroup/add/$', 'productgroup.add'),
                       url(r'^productgroup/add_ajax/$', 'productgroup.add_ajax'),
                       url(r'^productgroup/(?P<id>\d+)/edit/$', 'productgroup.edit'),
                       url(r'^productgroup/(?P<id>\d+)/delete/$', 'productgroup.delete'),

                       #Currency
                       url(r'^currency/$', 'currency.overview'),
                       url(r'^currency/add/$', 'currency.add'),
                       url(r'^currency/add_ajax/$', 'currency.add_ajax'),
                       url(r'^currency/(?P<id>\d+)/edit/$', 'currency.edit'),
                       url(r'^currency/(?P<id>\d+)/delete/$', 'currency.delete'),
                    )