from django.core import urlresolvers
from django.db import models
from app.projects.models import Project
from app.customers.models import Customer
from core.models import User, PersistentModel
from django.utils.translation import ugettext as _

class ProductLine(PersistentModel):
    product = models.ForeignKey('stock.Product', related_name="product_lines")
    description = models.TextField()
    count = models.IntegerField()
    price = models.CharField(max_length=10)

    def __unicode__(self):
        return "%s,%s" % (self.order, self.product)

class OrderBase(PersistentModel):
    title = models.CharField(_("Title"), max_length=80)
    customer = models.ForeignKey(Customer, related_name="orders", verbose_name=_("Customer"), blank=True, null=True)
    project = models.ForeignKey(Project, related_name="orders", verbose_name=_("Project"), blank=True, null=True)
    description = models.TextField(_("Description"))
    delivery_address = models.CharField(max_length=150, null=True)
    PO_number = models.CharField(_("PO-number"), max_length=150, blank=True, null=True)
    delivery_date = models.DateField(verbose_name=_("Delivery date"), null=True, blank=True)
    delivery_date_deadline = models.DateField(verbose_name=_("Delivery deadline"), null=True, blank=True)
    price = models.IntegerField(default=0)
    product_lines = models.ManyToManyField(ProductLine, related_name="%(class)s")
    
    def __unicode__(self):
        return self.title

class Invoice(OrderBase):
    invoice_number = models.IntegerField()
    order = models.ForeignKey('Order', related_name="invoices")

class Offer(OrderBase):
    offer_number = models.IntegerField()

class Order(OrderBase):
    order_number = models.IntegerField()
    offer = models.ForeignKey('Offer', related_name="orders", null=True, blank=True)

    def get_view_url(self):
        return urlresolvers.reverse('app.orders.views.view', args=("%s" % self.id,))