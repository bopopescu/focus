from django.conf.urls.defaults import *
from piston.resource import Resource
from api.authentication import TimeBasicAPIAuthentication
from api.contactsapi.handlers import ContactHandler
from api.customersapi.handlers import CustomersHandler
from api.hourregistrationsapi.handlers import HourRegistrationHandler
from api.productsapi.handlers import ProductsHandler

auth = TimeBasicAPIAuthentication()

contact = Resource(handler=ContactHandler, authentication=auth)
customers = Resource(handler=CustomersHandler, authentication=auth)
products = Resource(handler=ProductsHandler, authentication=auth)
hours = Resource(handler=HourRegistrationHandler, authentication=auth)

urlpatterns = patterns('',
                       url(r'contacts/$', contact),
                       url(r'contacts/(?P<id>\d+)/$', contact),

                       url(r'customers/$', customers),
                       url(r'customers/(?P<id>\d+)/$', customers),

                       url(r'hourregistrations/$', hours),
                       url(r'hourregistrations/(?P<id>\d+)/$', hours),

                       url(r'products/$', products),
                       url(r'products/(?P<id>\d+)/$', products),
)