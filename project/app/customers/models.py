from django.db import models
from core import Core
from core.models import PersistentModel
from django.core import urlresolvers
from core.models import User
from django.utils.translation import ugettext as _
from app.contacts.models import Contact

class Customer(PersistentModel):
    cid = models.IntegerField(_("Customer number"))
    full_name = models.CharField(_("Full name"), max_length=80)
    email = models.EmailField(_("E-mail"), max_length=80)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    website = models.CharField(_("Website"), max_length=150, blank=True, null=True)

    #Delivery and visit
    address = models.CharField(_("Address"), max_length=80, blank=True)
    zip = models.CharField(_("Area code"), max_length=15, blank=True)
    city = models.CharField(_("City"), max_length=20, blank=True)

    #Invoice
    invoice_address = models.CharField(_("Invoice address"), max_length=80, blank=True)
    invoice_zip = models.CharField(_("Invoice area code"), max_length=15, blank=True)
    invoice_city = models.CharField(_("Invoice city"), max_length=20, blank=True)

    contacts = models.ManyToManyField(Contact, blank=True, related_name="customers", verbose_name=_("Contacts"))

    def __unicode__(self):
        return self.full_name

    def canBeDeleted(self):
        canBeDeleted = True
        reasons = []

        if self.orders.all().count() > 0:
            canBeDeleted = False
            reasons.append(_("Customer has active orders"))

        if self.projects.all().count() > 0:
            canBeDeleted = False
            reasons.append(_("Customer has active projects"))

        if canBeDeleted:
            return (True, "OK")

        return (False, reasons)


    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.customers.views.add_ajax')

    @staticmethod
    def simpleform():
        return CustomerFormSimple(instance=Customer(), prefix="customers")

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Customer, self).save()

    def getViewUrl(self):
        return urlresolvers.reverse('app.customers.views.view', args=("%s" % self.id,))

from forms import CustomerFormSimple