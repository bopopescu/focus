from piston.handler import BaseHandler
from piston.utils import rc
from app.customers.forms import CustomerForm
from app.customers.models import Customer
from core import Core

class CustomersHandler(BaseHandler):
    model = Customer
    fields = ('id', 'cid', 'name', 'email', 'phone', 'website', 'address', 'zip', 'city', 'invoice_address', 'invoice_zip',
              'invoice_city', ('contacts', ('id', 'name'), ))


    def read(self, request, id=None):
        all = Core.current_user().get_permitted_objects("VIEW", Customer).filter(trashed=False)
        if id:
            try:
                return all.get(id=id)
            except Customer.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all


    def create(self, request):
        instance = Customer()
        form = CustomerForm(request.POST, instance=instance)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.owner = request.user
            form.save()
            form.save_m2m()
            return customer
        else:
            return form.errors


    def update(self, request, id):
        try:
            customer = Core.current_user().get_permitted_objects("EDIT", Customer).filter(trashed=False).get(id=id)
        except Customer.DoesNotExist:
            return rc.NOT_FOUND

        form = CustomerForm(request.PUT, instance=customer)
        if form.is_valid():
            form.save()
            return customer
        else:
            return form.errors


    def delete(self, request, id):
        try:
            customer = Core.current_user().get_permitted_objects("EDIT", Customer).filter(trashed=False).get(id=id)
        except Customer.DoesNotExist:
            return rc.NOT_FOUND

        if not customer.can_be_deleted()[0]:
            response = rc.FORBIDDEN
            for reason in customer.can_be_deleted()[1]:
                response.write(reason)
            return response
        else:
            customer.trash()
            return rc.DELETED



