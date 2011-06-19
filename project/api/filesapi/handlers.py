from app.files.forms import FileForm
from app.files.models import File
from piston.handler import BaseHandler
from app.contacts.models import Contact
from app.stock.models import Product
from core import Core
from piston.utils import rc

class FileHandler(BaseHandler):
    model = File
    fields = ('id', 'name', 'date_created', 'date_edited', ('editor', ('id', 'first_name', 'last_name')), 'get_file',
                  ('revisions', (
                  'id', 'name', ('editor', ('id', 'first_name', 'last_name')), 'date_created', 'date_edited',
                  'get_file'))) 

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", File).filter(trashed=False, )
        if id:
            try:
                return all.get(id=id)
            except File.DoesNotExist:
                return rc.NOT_FOUND

        return all

    def create(self, request, id=None):
        clone = None

        if id:
            instance = File.objects.get(id=id)
            clone = instance.clone()

        else:
            instance = File()

        form = FileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.owner = request.user
            form.save()

            if id:
                clone.save()

            return customer

        else:
            return form.errors