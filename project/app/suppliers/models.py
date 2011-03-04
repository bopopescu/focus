from django.db import models
from core import Core
from core.models import PersistentModel
from app.contacts.models import Contact
from django.core import urlresolvers

class Supplier(PersistentModel):
    name = models.CharField(max_length=200)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField(null=True)

    contacts = models.ManyToManyField(Contact, related_name="suppliers")

    def __unicode__(self):
        return self.name

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.suppliers.views.add_ajax')

    @staticmethod
    def simpleform():
        return SupplierSimpleForm(instance=Supplier(), prefix="suppliers")

    def getViewUrl(self):
        return urlresolvers.reverse('app.suppliers.views.view', args=("%s" % self.id,))

    def getEditUrl(self):
        return urlresolvers.reverse('app.suppliers.views.edit', args=("%s" % self.id,))

    def getHistoryUrl(self):
      return urlresolvers.reverse('app.suppliers.views.history', args=("%s" % self.id,))
  
    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Supplier, self).save()

from app.suppliers.forms import SupplierSimpleForm