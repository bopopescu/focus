from django.conf.urls.defaults import *

urlpatterns = patterns('app.admin.views',

                       #User
                       url(r'^users/$', 'user.overview'),
                       url(r'^user/add/$', 'user.add'),
                       url(r'^user/(?P<id>\d+)/edit/$', 'user.edit'),
                       url(r'^user/(?P<id>\d+)/view/$', 'user.view'),
                       url(r'^user/(?P<id>\d+)/delete/$', 'user.delete'),
                       url(r'^user/(?P<id>\d+)/changeCanLogin/$', 'user.changeCanLogin'),
                       url(r'^user/(?P<id>\d+)/sendNewPassword/', 'user.sendGeneratedPassword'),
                       url(r'^user/(?P<id>\d+)/manualSetTime/$', 'user.setHourRegistrationLimitsManually'),

                       #Group
                       url(r'^groups/$', 'group.overview'),
                       url(r'^groups/add/$', 'group.add'),
                       url(r'^group/(?P<id>\d+)/edit/$', 'group.edit'),
                       url(r'^group/(?P<id>\d+)/view/$', 'group.view'),
                       url(r'^group/(?P<id>\d+)/delete/$', 'group.delete'),

                       #Company
                       url(r'^company/', 'company.editCompany'),

                       #Profle
                       url(r'^profile/edit/$', 'profile.edit'),
                       url(r'^profile/password/$', 'profile.changePassword'),
                       url(r'^profile/image/$', 'profile.changeProfileImage'),
                       )

