from django.conf.urls.defaults import *
from piston.resource import Resource
from api.authentication import TimeBasicAPIAuthentication
from api.contactsapi.handlers import ContactHandler
from api.customersapi.handlers import CustomersHandler

auth = TimeBasicAPIAuthentication()

contact = Resource(handler=ContactHandler, authentication=auth)
customers = Resource(handler=CustomersHandler, authentication=auth)

urlpatterns = patterns('',
   url(r'contacts/$', contact),
   url(r'contacts/(?P<id>\d+)/$', contact),

   url(r'customers/$', customers),
   url(r'customers/(?P<id>\d+)/$', customers),

)
