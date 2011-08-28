from django.conf.urls.defaults import *
from piston.emitters import Emitter
from api.filesapi.handlers import FileHandler, FileTagHandler
from api.projectsapi.handlers import ProjectHandler
from piston.resource import Resource
from api.authentication import TimeBasicAPIAuthentication
from api.contactsapi.handlers import ContactHandler
from api.customersapi.handlers import CustomersHandler
from api.hourregistrationsapi.handlers import HourRegistrationHandler, TimeTrackerHandler
from api.ticketsapi.handlers import TicketHandler
from api.productsapi.handlers import ProductsHandler

auth = TimeBasicAPIAuthentication()

contact = Resource(handler=ContactHandler, authentication=auth)
customers = Resource(handler=CustomersHandler, authentication=auth)
hours = Resource(handler=HourRegistrationHandler, authentication=auth)
timetracker = Resource(handler=TimeTrackerHandler, authentication=auth)
tickets = Resource(handler=TicketHandler, authentication=auth)
products = Resource(handler=ProductsHandler, authentication=auth)
projects = Resource(handler=ProjectHandler, authentication=auth)
files = Resource(handler=FileHandler, authentication=auth)
filetags = Resource(handler=FileTagHandler, authentication=auth)

urlpatterns = patterns('',
                       #Contacts
                       url(r'contacts/$', contact),
                       url(r'contacts/(?P<id>\d+)/$', contact),

                       #Customers
                       url(r'customers/$', customers),
                       url(r'customers/(?P<id>\d+)/$', customers),

                       #Projects
                       url(r'projects/$', projects),
                       url(r'projects/(?P<id>\d+)/$', projects),

                       #Hourregistration
                       url(r'hourregistrations/$', hours),
                       url(r'hourregistrations/(?P<id>\d+)/$', hours),
                       url(r'timetracker/$', timetracker, name='timetracker_all'),
                       url(r'timetracker/(?P<id>\d+)/$', timetracker, name='timetracker_instance'),

                       #Tickets
                       url(r'tickets/$', tickets, {'emitter_format': 'json-cached'}),
                       url(r'tickets/(?P<id>\d+)/$', tickets, {'emitter_format': 'json-cached'}),

                       #Files
                       url(r'files/$', files),
                       url(r'files/(?P<id>\d+)/$', files),

                       url(r'filetags/$', filetags),
                       url(r'filetags/(?P<id>\d+)/$', filetags),

                       #Products
                       url(r'products/$', products),
                       url(r'products/(?P<id>\d+)/$', products),
                    )
