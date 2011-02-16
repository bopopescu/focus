# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('app.projects.views',

                       #Project
                       url(r'^$', 'project.overview'),
                       url(r'^timeline/?$', 'project.timeline'),
                       url(r'^deleted/?$', 'project.overview_trashed'),
                       url(r'^all/?$', 'project.overview_all'),
                       url(r'^add/$', 'project.add'),
                       url(r'^add_ajax/$', 'project.add_ajax'),
                       url(r'^(?P<id>\d+)/edit/?$', 'project.edit'),
                       url(r'^(?P<id>\d+)/view/?$', 'project.view'),
                       url(r'^(?P<id>\d+)/delete/?$', 'project.delete'),
                       url(r'^(?P<id>\d+)/history/?$', 'project.history'),

                       #Milestone

                       url(r'^(?P<project_id>\d+)/add_milestone/$', 'milestone.add'),
                       url(r'^(?P<project_id>\d+)/edit_milestone/(?P<milestone_id>\d+)$', 'milestone.edit'),

                       )