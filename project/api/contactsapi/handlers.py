from piston.handler import BaseHandler
from app.contacts.forms import ContactForm
from app.contacts.models import Contact
from core import Core
from piston.utils import rc

class ContactsCollectionHandler(BaseHandler):
    model = Contact

    def read(self, request):
        return Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=False)


    def create(self, request):
        instance = Contact()
        form = ContactForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            form.save_m2m()
            return contact
        else:
            return form.errors



class ContactHandler(BaseHandler):
    model = Contact

    def read(self, request, id):
        try:
            contact = Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=False).get(id=id)
        except Contact.DoesNotExist:
            return rc.NOT_FOUND
        return contact


    def update(self, request, id):
        try:
            contact = Core.current_user().get_permitted_objects("EDIT", Contact).filter(trashed=False).get(id=id)
        except Contact.DoesNotExist:
            return rc.NOT_FOUND

        form = ContactForm(request.PUT, request.FILES, contact)
        if form.is_valid():
            form.save()
        else:
            return form.errors

    def delete(self, request, id):
        try:
            contact = Core.current_user().get_permitted_objects("DELETE", Contact).filter(trashed=False).get(id=id)
        except Contact.DoesNotExist:
            return rc.NOT_FOUND

        if not contact.can_be_deleted()[0]:
            response = rc.FORBIDDEN #Maybe better to return 200 OK with JSON error information?
            for reason in contact.can_be_deleted()[1]:
                response.write(reason)
            return response
        else:
            contact.trash()
            return rc.DELETED











    
