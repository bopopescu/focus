from django.conf.urls.defaults import *
from piston.resource import Resource
from api.authentication import TimeBasicAPIAuthentication
from api.contactsapi.handlers import ContactsCollectionHandler, ContactHandler

auth = TimeBasicAPIAuthentication()

contacts_collection = Resource(handler=ContactsCollectionHandler, authentication=auth)
contact = Resource(handler=ContactHandler, authentication=auth)

urlpatterns = patterns('',
   url(r'contacts/$', contacts_collection),
   url(r'contacts/(?P<id>\d+)$', contact),
)
