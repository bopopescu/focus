from piston.handler import BaseHandler
from app.contacts.forms import ContactForm
from app.contacts.models import Contact
from core import Core
from piston.utils import rc

class ContactHandler(BaseHandler):
    model = Contact
    fields = ('id', 'full_name', 'address', 'email', 'phone', 'phone_office', 'phone_mobile', 'description',
              ('comments', ('text', ),), ('customers', ('id', 'full_name',),), )


    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=False)
        if id:
            try:
                return all.get(id=id)
            except Contact.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all

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


    def update(self, request, id):
        try:
            contact = Core.current_user().get_permitted_objects("EDIT", Contact).filter(trashed=False).get(id=id)
        except Contact.DoesNotExist:
            return rc.NOT_FOUND

        form = ContactForm(request.PUT, request.FILES, instance=contact)
        if form.is_valid():
            form.save()
            return contact
        else:
            return form.errors


    def delete(self, request, id):
        try:
            contact = Core.current_user().get_permitted_objects("DELETE", Contact).filter(trashed=False).get(id=id)
        except Contact.DoesNotExist:
            return rc.NOT_FOUND

        if not contact.can_be_deleted()[0]:
            response = rc.FORBIDDEN #Maybe better to return 200 OK with error information?
            for reason in contact.can_be_deleted()[1]:
                response.write(reason)
            return response
        else:
            contact.trash()
            return rc.DELETED












    
