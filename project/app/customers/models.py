# -*- coding: utf-8 -*-
from django.db import models
from core import Core
from core.models import PersistentModel, Comment
from django.core import urlresolvers
from core.models import User
from django.utils.translation import ugettext as _
from app.contacts.models import Contact
from django.db.models.aggregates import Max
from django.contrib.contenttypes import generic

class Customer(PersistentModel):
    cid = models.IntegerField(_("Customer number"))
    name = models.CharField(_("Name"), max_length=80)
    email = models.EmailField(_("E-mail"), max_length=80)
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    website = models.CharField(_("Website"), max_length=150, blank=True, null=True)

    #Delivery and visit
    address = models.TextField(_("Address"), blank=True)
    zip = models.CharField(_("Zip"), max_length=15, blank=True)

    #Invoice
    invoice_address = models.TextField(_("Invoice address"), blank=True)
    invoice_zip = models.CharField(_("Invoice zip"), max_length=15, blank=True)

    contacts = models.ManyToManyField(Contact, blank=True, related_name="customers", verbose_name=_("Contacts"))

    comments = generic.GenericRelation(Comment)


    def __unicode__(self):
        return self.name

    @staticmethod
    def calculate_next_cid():
        next = (Customer.objects.filter_current_company().aggregate(Max("cid"))['cid__max'])
        if next:
            return next + 1
        return 1

    def can_be_deleted(self):
        can_be_deleted = True
        reasons = []

        if self.orders.all().count() > 0:
            can_be_deleted = False
            reasons.append(_("Customer has active orders"))

        if self.projects.all().count() > 0:
            can_be_deleted = False
            reasons.append(_("Customer has active projects"))

        if can_be_deleted:
            return (True, "OK")

        return (False, reasons)

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.customers.views.add_ajax')

    @staticmethod
    def simpleform():
        return CustomerFormSimple(instance=Customer(), prefix="customers", initial= {'cid':Customer.calculate_next_cid()})

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Customer, self).save()

    def get_view_url(self):
        return urlresolvers.reverse('app.customers.views.view', args=("%s" % self.id,))

from forms import CustomerFormSimple