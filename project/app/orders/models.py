# -*- coding: utf-8 -*-
from django.core import urlresolvers
from django.db import models
from app.files.models import File
from django.contrib.contenttypes import generic
from app.orders.managers import OrderArchivedManager, OrderManager
from app.projects.models import Project
from app.customers.models import Customer
from core.models import  PersistentModel, Comment
from django.utils.translation import ugettext as _
from django.db.models.aggregates import Max

class ProductLine(models.Model):
    product = models.ForeignKey('stock.Product', related_name="product_lines", verbose_name=_("Product"), null=True, blank=True, default=None)
    description = models.TextField(_("Description"))
    count = models.IntegerField(_("Count"))
    price = models.CharField(_("Price"), max_length=10)

    def __unicode__(self):
        return self.description

class OrderBase(PersistentModel):
    title = models.CharField(_("Title"), max_length=80)
    customer = models.ForeignKey(Customer, related_name="orders", verbose_name=_("Customer"), blank=True, null=True)
    project = models.ForeignKey(Project, related_name="orders", verbose_name=_("Project"), blank=True, null=True)
    description = models.TextField(_("Description"))
    delivery_address = models.CharField(_("Delivery address"), max_length=150, null=True)
    PO_number = models.CharField(_("PO-number"), max_length=150, blank=True, null=True)
    delivery_date = models.DateField(verbose_name=_("Delivery date"), null=True, blank=True)
    delivery_date_deadline = models.DateField(verbose_name=_("Delivery deadline"), null=True, blank=True)
    price = models.IntegerField(_("Price"), default=0)
    archived = models.BooleanField(default=False, verbose_name=_("Archived"))
    product_lines = models.ManyToManyField(ProductLine, related_name="%(class)s")
    files = models.ManyToManyField(File)
    comments = generic.GenericRelation(Comment)

    def copy_from(self, object):
        self.title = object.title
        self.customer = object.customer
        self.project = object.project
        self.description = object.description
        self.delivery_address = object.delivery_address
        self.PO_number = object.PO_number
        self.delivery_date = object.delivery_date
        self.delivery_date_deadline = object.delivery_date_deadline
        self.price = object.price
        self.archived = object.archived

        self.save()

        if self.id:
            self.update_products(object.product_lines.all())

    def update_products(self, products):
        self.product_lines.clear()

        for p in products:
            p.save()
            self.product_lines.add(p)

        self.save()

    def __unicode__(self):
        return self.title


class Invoice(OrderBase):
    invoice_number = models.IntegerField(_("Invoice number"))
    order = models.ForeignKey("Order", verbose_name=_("Order"), related_name="invoices")

    def get_view_url(self):
        return urlresolvers.reverse('app.invoices.views.view', args=("%s" % self.id,))


    @staticmethod
    def calculate_next_invoice_number():
        next = (Invoice.objects.filter_current_company().aggregate(Max("invoice_number"))['invoice_number__max'])
        if next:
            return next + 1
        return 1


accepted_choices = (
            (True,"True"),
            (False,"False"),
        )

class Offer(OrderBase):
    offer_number = models.IntegerField(_("Offer number"))
    accepted = models.NullBooleanField(default=None, choices=accepted_choices, verbose_name=_("Accepted"))

    def get_view_url(self):
        return urlresolvers.reverse('app.offers.views.view', args=("%s" % self.id,))

    def get_accepted_status(self):
        if self.accepted is None:
            return _("Pending reply"), "orange"
        if self.accepted:
            return _("Accepted"), "green"

        return _("Declined"), "red"

    @staticmethod
    def calculate_next_offer_number():
        next = (Offer.objects.filter_current_company().aggregate(Max("offer_number"))['offer_number__max'])
        if next:
            return next + 1
        return 1


class Order(OrderBase):
    order_number = models.IntegerField(_("Order number"))
    offer = models.ForeignKey('orders.Offer', verbose_name=_("Offer"), related_name="orders", null=True, blank=True)

    #Managers
    objects = OrderManager()
    archived_objects = OrderArchivedManager()
    all_objects = models.Manager()

    @staticmethod
    def calculate_next_order_number():
        next = (Order.objects.filter_current_company().aggregate(Max("order_number"))['order_number__max'])
        if next:
            return next + 1
        return 1

    def get_view_url(self):
        return urlresolvers.reverse('app.orders.views.view', args=("%s" % self.id,))
