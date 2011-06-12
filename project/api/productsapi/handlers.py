from app.stock.forms import ProductFileForm
from piston.handler import BaseHandler
from app.contacts.forms import ContactForm
from app.contacts.models import Contact
from app.stock.models import Product, ProductFile
from core import Core
from piston.utils import rc

class ProductsHandler(BaseHandler):
    model = Product
    fields = ('id', 'name', 'description', 'price_out', ('files', ('id', 'name', ('editor', ('first_name','last_name')), 'date_created','date_edited', 'get_file')))

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Product).filter(trashed=False)
        if id:
            try:
                return all.get(id=id)
            except Contact.DoesNotExist:
                return rc.NOT_FOUND
        else:
            all = ProductsHandler.filter_products(all, request.GET)

        return all

    @staticmethod
    def filter_products(products, filter):
        name_startswith = (filter.get('name_startsWith', False))
        if name_startswith:
            products = products.filter(name__icontains=name_startswith)

        return products


class ProductfilesHandler(BaseHandler):
    model = ProductFile
    fields = ('id', 'name', ('product',('id', 'name')),'trashed','date_created',('editor', ('first_name','last_name')),'date_edited', 'get_file',('history', ('id', 'name',('editor', ('first_name','last_name')), 'trashed','date_created', 'date_edited','get_file')))

    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", ProductFile).filter(trashed=False, parent=None)
        if id:
            try:
                return all.get(id=id)
            except ProductFile.DoesNotExist:
                return rc.NOT_FOUND
        else:
            all = ProductsHandler.filter_products(all, request.GET)

        return all

    def create(self, request, id=None):

        if id:
            instance = ProductFile.objects.get(id=id)
            clone = instance.clone()

        else:
            instance = ProductFile()
                
        form = ProductFileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.owner = request.user
            form.save()
            if id:
                clone.save()

            form.save_m2m()
            return customer
        else:
            return form.errors