# -*- coding: utf-8 -*-
from app.calendar.models import Event
from core.auth.user.models import User
from core.cache import cachedecorator
from django.core.cache import cache
from django.core import urlresolvers
from django.core.exceptions import ValidationError
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
    product = models.ForeignKey('stock.Product', related_name="product_lines", verbose_name=_("Product"), null=True,
                                blank=True, default=None)
    description = models.TextField(_("Description"))
    count = models.IntegerField(_("Count"), default=0)
    price = models.CharField(_("Price"), max_length=10, default=0)
    tax = models.CharField(_("Price"), max_length=10, default=0)

    def __unicode__(self):
        return self.description

    def get_item(self):
        if self.product:
            return self.product
        return "Item"

    def get_total_sum(self):
        if self.count and self.price:
            return int(self.count) * int(self.price)
        return 0


class OrderBase(PersistentModel):
    title = models.CharField(_("Title"), max_length=80)
    customer = models.ForeignKey(Customer, related_name="orders", verbose_name=_("Customer"), blank=True, null=True)
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

    @cachedecorator('get_customer')
    def get_customer(self):
        return self.customer

    @cachedecorator('get_project')
    def get_project(self):
        return self.project

    def invalidate_cache(self):
        cache.delete("cachedecorator_%s_%s_%s" % (self.__class__.__name__, self.pk, "get_customer"))
        cache.delete("cachedecorator_%s_%s_%s" % (self.__class__.__name__, self.pk, "get_project"))

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
            if not p.id:
                if p.product or p.description:
                    if not p.count:
                        p.count = 1

                    if not p.price:
                        p.price = 0

                    if not p.tax:
                        p.price = 0

                    p.save()

            if p.id:
                self.product_lines.add(p)

    def save(self, **kwargs):
        super(OrderBase, self).save()
        self.invalidate_cache()

    def __unicode__(self):
        return self.title


invoice_status_choices = (
    ("0", _("New")),
    ("1", _("Sent")),
    ("2", _("Paid")),
    )

class Invoice(OrderBase):
    invoice_number = models.IntegerField(_("Invoice number"))
    order = models.ForeignKey("Order", verbose_name=_("Order"), related_name="invoices")
    project = models.ForeignKey(Project, related_name="invoices", verbose_name=_("Project"), blank=True, null=True)
    status = models.CharField(default=None, null=True, max_length=10, choices=invoice_status_choices,
                              verbose_name=_("Status"))

    def get_view_url(self):
        return urlresolvers.reverse('app.invoices.views.view', args=("%s" % self.id,))

    @staticmethod
    def calculate_next_invoice_number():
        next = (Invoice.objects.filter_current_company().aggregate(Max("invoice_number"))['invoice_number__max'])
        if next:
            return next + 1
        return 1.0

offer_status_choices = (
    ("0", _("Pending")),
    ("1", _("Accepted")),
    ("2", _("Declined")),
    )

class Offer(OrderBase):
    offer_number = models.CharField(_("Offer number"), max_length=150, default="")
    accepted = models.CharField(max_length=5, null=True, default=None, choices=offer_status_choices,
                                verbose_name=_("Accepted"))
    project = models.ForeignKey(Project, related_name="offers", verbose_name=_("Project"), blank=True, null=True)

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
        try:
            next = (Offer.objects.filter_current_company().aggregate(Max("offer_number"))['offer_number__max'])
            if next:
                return next + 1
            return 1.0
        except Exception, e:
            return ""

order_status_choices = (
    ("0", _("New")),
    ("1", _("In progress")),
    ("2", _("Done")),
    )

class Order(OrderBase):
    order_number = models.CharField(_("Order number"), max_length=150, default="")
    offer = models.ForeignKey('orders.Offer', verbose_name=_("Offer"), related_name="orders", null=True, blank=True)
    project = models.ForeignKey(Project, related_name="orders", verbose_name=_("Project"), blank=True, null=True)

    status = models.CharField(default=None, null=True, max_length=10, choices=order_status_choices,
                              verbose_name=_("Status"))

    events = models.ManyToManyField(Event, related_name="orders")

    #Managers
    objects = OrderManager()
    archived_objects = OrderArchivedManager()
    all_objects = models.Manager()

    @staticmethod
    def calculate_next_order_number():
        try:
            next = (Order.objects.filter_current_company().aggregate(Max("order_number"))['order_number__max'])
            if next:
                return next + 1
            return 1.0
        except Exception, e:
            return ""

    def get_view_url(self):
        return urlresolvers.reverse('app.orders.views.order.view', args=("%s" % self.id,))


class OrderMembership(PersistentModel):
    order = models.ForeignKey(Order, related_name="memberships")
    user = models.ForeignKey(User, related_name="orders_memberships")
    description = models.TextField()
    work_done = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s member of %s " % (self.user, self.order)
