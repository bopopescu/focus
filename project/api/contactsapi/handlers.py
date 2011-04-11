from piston.handler import BaseHandler
from piston.utils import validate
from app.contacts.forms import ContactForm
from app.contacts.models import Contact
from core import Core
from piston.utils import rc

class ContactHandler(BaseHandler):
    model = Contact

    def read(self, request):
        return Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=False)


    #@validate(ContactForm)
    def create(self, request):
        instance = Contact()
        form = ContactForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.owner = request.user
            o.save()
            form.save_m2m()
            return o
        else:
            print form.errors
            return rc.BAD_REQUEST





    
