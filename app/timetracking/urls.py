from django.conf.urls.defaults import *

urlpatterns = patterns('app.timetracking.views',

        url(r'^$', 'overview'),
        url(r'^add/$', 'add'), 
        url(r'^edit/(\d+)/?$', 'edit'),
        url(r'^delete/(\d+)/?$', 'delete'),
        url(r'^calendar/',      'calendar'),
        


        #Ajax

        url(r'^ajaxResizeCalendar/$', 'ajaxResizeCalendar'),

        url(r'^ajaxAddCalendar/$', 'ajaxAddCalendar'),




)