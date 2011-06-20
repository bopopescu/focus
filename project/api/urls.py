from django.conf.urls.defaults import *
from piston.resource import Resource
from api.authentication import TimeBasicAPIAuthentication
from api.contactsapi.handlers import ContactHandler
from api.customersapi.handlers import CustomersHandler
from api.hourregistrationsapi.handlers import HourRegistrationHandler, TimeTrackerHandler
from api.ticketsapi.handlers import TicketHandler
from api.productsapi.handlers import ProductsHandler, ProductfilesHandler

auth = TimeBasicAPIAuthentication()

contact = Resource(handler=ContactHandler, authentication=auth)
customers = Resource(handler=CustomersHandler, authentication=auth)
hours = Resource(handler=HourRegistrationHandler, authentication=auth)
timetracker = Resource(handler=TimeTrackerHandler, authentication=auth)
tickets = Resource(handler=TicketHandler, authentication=auth)
products = Resource(handler=ProductsHandler, authentication=auth)
productfiles = Resource(handler=ProductfilesHandler, authentication=auth)

urlpatterns = patterns('',
                       #Contacts
                       url(r'contacts/$', contact),
                       url(r'contacts/(?P<id>\d+)/$', contact),

                       #Customers
                       url(r'customers/$', customers),
                       url(r'customers/(?P<id>\d+)/$', customers),

                       #Hourregistration
                       url(r'hourregistrations/$', hours),
                       url(r'hourregistrations/(?P<id>\d+)/$', hours),
                       url(r'timetracker/$', timetracker, name='timetracker_all'),
                       url(r'timetracker/(?P<id>\d+)/$', timetracker, name='timetracker_instance'),


                       #Tickets
                       url(r'tickets/$', tickets),
                       url(r'tickets/(?P<id>\d+)/$', tickets),


                       #Products
                       url(r'products/$', products),
                       url(r'products/(?P<id>\d+)/$', products),

                       #ProductFiles
                       url(r'productfiles/$', productfiles),
                       url(r'productfiles/(?P<id>\d+)/$', productfiles),
)