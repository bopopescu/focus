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
('Offer', _('Offer')),
("Invoice", _("Ready for Invoice")),
("Archive", _("Archived")),
)

class Order(PersistentModel):
    oid = models.IntegerField(_("Order number"), null=True, blank=True)
    POnumber = models.CharField(_("PO-number"), max_length=150, blank=True, null=True)
    order_name = models.CharField(_("Name"), max_length=80)
    customer = models.ForeignKey(Customer, related_name="orders", verbose_name=_("Customer"), blank=True, null=True)
    project = models.ForeignKey(Project, related_name="orders", verbose_name=_("Project"), blank=True, null=True)
    deliveryAddress = models.CharField(max_length=150, null=True)
    responsible = models.ForeignKey(User, related_name="ordersWhereResponsible", verbose_name=_("Responsible"))
    delivery_date = models.DateField(verbose_name=_("Delivery date"), null=True, blank=True)
    delivery_date_deadline = models.DateField(verbose_name=_("Delivery deadline"), null=True, blank=True)
    description = models.TextField(_("Description"))
    contacts = models.ManyToManyField(Contact, related_name="orders", verbose_name=_("Contacts"), blank=True)

    state = models.CharField(max_length=10, choices=STATUS_CHOICES)

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

    def is_offer(self):
        if self.state == "Offer":
            return True
        return False

    def is_order(self):
        if self.state == "Order":
            return True
        return False

    def is_valid_for_edit(self):
        if self.is_offer():
            return True
        if self.is_order():
            return True
        return False

    def getViewUrl(self):
        return urlresolvers.reverse('app.orders.views.view', args=("%s" % self.id,))

    def haveCompletedAllTasks(self):
        tasks = self.tasks

        for t in tasks.all():
            if not t.done:
                return False

        return True

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Order, self).save()

class OrderLine(PersistentModel):
    order = models.ForeignKey(Order, related_name="orderlines")
    product = models.ForeignKey('stock.Product', related_name="orderlines")
    count = models.IntegerField()

    def __unicode__(self):
        return "Order: %s, Product: %s" % (self.order, self.product)

class Task(PersistentModel):
    order = models.ForeignKey(Order, related_name="tasks")
    text = models.TextField("Ny oppgave")
    done = models.BooleanField(default=False)

    def __unicode__(self):
        return self.text

class OrderFolder(PersistentModel):
    project_id = models.ForeignKey(Order, related_name="folders")
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "Prosjektmappe: %s" % self.name

class OrderFile(PersistentModel):
    project_id = models.ForeignKey(Order, related_name="files")
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(OrderFolder, related_name="files")

    def __unicode__(self):
        return "Prosjektfil: %s" % self.name