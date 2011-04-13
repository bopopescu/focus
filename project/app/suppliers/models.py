from django.db import models
from core import Core
from core.models import PersistentModel
from app.contacts.models import Contact
from django.core import urlresolvers
from django.utils.translation import ugettext as _

class Supplier(PersistentModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=40, null=True)
    address = models.TextField(null=True)
    zip = models.CharField(max_length=10, default="")
    email_contact = models.EmailField(default="")
    email_order = models.EmailField(default="")
    country = models.CharField(max_length=20, default="")
    reference = models.CharField(max_length=150, default="")
    contacts = models.ManyToManyField(Contact, related_name="suppliers")

    def __unicode__(self):
        return self.name


    def can_be_deleted(self):
        can_be_deleted = True
        reasons = []

        if self.products.all().count() > 0:
            can_be_deleted = False
            reasons.append(_("Supplier has active products"))

        if can_be_deleted:
            return (True, "OK")

        return (False, reasons)

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.suppliers.views.add_ajax')

    @staticmethod
    def simpleform():
        return SupplierSimpleForm(instance=Supplier(), prefix="suppliers")

    def get_view_url(self):
        return urlresolvers.reverse('app.suppliers.views.view', args=("%s" % self.id,))

    def get_edit_url(self):
        return urlresolvers.reverse('app.suppliers.views.edit', args=("%s" % self.id,))

    def get_history_url(self):
        return urlresolvers.reverse('app.suppliers.views.history', args=("%s" % self.id,))

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Supplier, self).save()

from app.suppliers.forms import SupplierSimpleForm