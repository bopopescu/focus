from piston.handler import BaseHandler
from app.contacts.forms import ContactForm
from app.contacts.models import Contact
from app.stock.models import Product
from core import Core
from piston.utils import rc

class ProductsHandler(BaseHandler):
    model = Product
    fields = ('id', 'name','description','price_out')


    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Product).filter(trashed=False)
        if id:
            try:
                return all.get(id=id)
            except Contact.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all