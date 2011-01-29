from django.core import urlresolvers
from django.db import models
from core import Core
from app.projects.models import Project
from app.customers.models import Customer
from app.contacts.models import Contact
from core.models import User, PersistentModel


class OrderState(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name

class Order(PersistentModel):
    oid = models.IntegerField("Ordrenr", null=True, blank=True)
    POnumber = models.CharField("PO-number", max_length=150, blank=True, null=True)
    order_name = models.CharField("Navn", max_length=80)
    customer = models.ForeignKey(Customer, related_name="orders", verbose_name="Kunde", blank=True, null=True)
    project = models.ForeignKey(Project, related_name="orders", verbose_name="Prosjekt", blank=True, null=True)
    deliveryAddress = models.CharField(max_length=150, null=True)
    responsible = models.ForeignKey(User, related_name="ordersWhereResponsible", verbose_name="Ansvarlig")
    delivery_date = models.DateField(verbose_name="Leveringsdato", null=True, blank=True)
    delivery_date_deadline = models.DateField(verbose_name="Leveringsfrist", null=True, blank=True)
    description = models.TextField("Beskrivelse")
    contacts = models.ManyToManyField(Contact, related_name="orders", verbose_name="Kontakter", blank=True)
    state = models.ForeignKey(OrderState)

    def __unicode__(self):
        return self.order_name

    def is_archived(self):
        if self.state == "Arkivert":
            return True
        return False

    def is_ready_for_invoice(self):
        if self.state == "Til faktura":
            return True
        return False

    def is_offer(self):
        if self.state == "Tilbud":
            return True
        return False

    def is_order(self):
        if self.state == "Ordre":
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

        #Give the user who created this ALL permissions on object

        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

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

def initial_data ():
    OrderState.objects.get_or_create(name="Tilbud")
    OrderState.objects.get_or_create(name="Arkiv")
    OrderState.objects.get_or_create(name="Ordre")
    OrderState.objects.get_or_create(name="Klar for faktura")
