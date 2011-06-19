# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('app.projects.views',
                       #Project
                       url(r'^$', 'project.overview'),
                       url(r'^timeline/?$', 'project.timeline'),
                       url(r'^deleted/?$', 'project.overview_trashed'),
                       url(r'^all/?$', 'project.overview_all'),
                       url(r'^add/$', 'project.add'),
                       url(r'^(?P<id>\d+)/edit/?$', 'project.edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'project.view'),
                       url(r'^(?P<id>\d+)/orders/?$', 'project.view_orders'),
                       url(r'^(?P<id>\d+)/trash/?$', 'project.trash'),
                       url(r'^(?P<id>\d+)/history/?$', 'project.history'),
                       url(r'^(?P<id>\d+)/milestones/?$', 'project.milestones'),

                       #Files
                       url(r'^(?P<id>\d+)/files/$', 'files.overview'),
                       url(r'^(?P<id>\d+)/files/add/$', 'files.add_file'),
                       url(r'^(?P<id>\d+)/files/(?P<file_id>\d+)/edit/$', 'files.edit_file'),

                       #Project ajax
                       url(r'^add_ajax/$', 'project_ajax.add'),
                       url(r'^list_ajax/$', 'project_ajax.list_by_customer'),
                       
                       #Milestone
                       url(r'^(?P<project_id>\d+)/add_milestone/$', 'milestone.add'),
                       url(r'^(?P<project_id>\d+)/edit_milestone/(?P<milestone_id>\d+)$', 'milestone.edit'),

                       )