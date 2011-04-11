from piston.handler import BaseHandler
from app.contacts.models import Contact
from core import Core

class ContactHandler(BaseHandler):
    model = Contact


    def read(self, request):
        return Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=False)
    
