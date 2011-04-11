from django.conf.urls.defaults import *
from piston.resource import Resource
from api.authentication import TimeBasicAPIAuthentication
from api.contactsapi.handlers import ContactHandler

auth = TimeBasicAPIAuthentication()

contacts = Resource(handler=ContactHandler, authentication=auth)


urlpatterns = patterns('',
   url(r'contacts/list$', contacts),
)
