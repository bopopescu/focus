from django.core import urlresolvers
from django.db import models
from core import Core
from app.projects.models import Project
from app.customers.models import Customer
from app.contacts.models import Contact
from core.models import User, PersistentModel
from django.utils.translation import ugettext as _

STATUS_CHOICES = (
('Order', _('Order')),
("Invoice", _("Ready for Invoice")),
("Archive", _("Archived")),
)

TYPE_CHOICES = (
('GARANTI', _("GUARANTY")),
("STANDARD", _("STANDARD")),
)

class Offer(PersistentModel):
    oid = models.IntegerField()
    title = models.CharField(max_length=40)
    description = models.TextField()
    price = models.IntegerField(default=0)
    delivery_date = models.DateField()
    approved = models.NullBooleanField(default=None, null=True, blank=True)
    recipient_email_address = models.CharField(max_length=60)
    earlier_version = models.ForeignKey("Offer")
    
    def __unicode__(self):
        return self.title

class OfferLine(PersistentModel):
    order = models.ForeignKey(Offer, related_name="offer_lines")
    product = models.ForeignKey('stock.Product', related_name="offer_lines")
    count = models.IntegerField()

    def __unicode__(self):
        return "Order: %s, Product: %s" % (self.order, self.product)
    
class Order(PersistentModel):
    oid = models.IntegerField(_("Order number"), null=True, blank=True)
    POnumber = models.CharField(_("PO-number"), max_length=150, blank=True, null=True)
    order_name = models.CharField(_("Name"), max_length=80)
    customer = models.ForeignKey(Customer, related_name="orders", verbose_name=_("Customer"), blank=True, null=True)
    project = models.ForeignKey(Project, related_name="orders", verbose_name=_("Project"), blank=True, null=True)
    deliveryAddress = models.CharField(max_length=150, null=True)
    responsible = models.ForeignKey(User, related_name="responsible_orders", verbose_name=_("Responsible"),
                                    null=True, blank=True)

    delivery_date = models.DateField(verbose_name=_("Delivery date"), null=True, blank=True)
    delivery_date_deadline = models.DateField(verbose_name=_("Delivery deadline"), null=True, blank=True)
    description = models.TextField(_("Description"))
    contacts = models.ManyToManyField(Contact, related_name="orders", verbose_name=_("Contacts"), blank=True)

    type = models.CharField(_("Type"), max_length=15, choices=TYPE_CHOICES, default="STANDARD")
    state = models.CharField(max_length=10, choices=STATUS_CHOICES)

    price = models.IntegerField(default=0)

    def __unicode__(self):
        return self.order_name

    def is_archived(self):
        if self.state == "Archive":
            return True
        return False

    def is_ready_for_invoice(self):
        if self.state == "Invoice":
            return True
        return False

    def is_order(self):
        if self.state == "Order":
            return True
        return False

    def is_valid_for_edit(self):
        if self.is_order():
            return True
        return False

    def get_view_url(self):
        return urlresolvers.reverse('app.orders.views.view', args=("%s" % self.id,))

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Order, self).save()

class OrderLine(PersistentModel):
    order = models.ForeignKey(Order, related_name="order_lines")
    product = models.ForeignKey('stock.Product', related_name="order_lines")
    count = models.IntegerField()

    def __unicode__(self):
        return "Order: %s, Product: %s" % (self.order, self.product)