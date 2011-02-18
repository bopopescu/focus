from core.models import PersistentModel, User, Comment
from django.db import models
from app.customers.models import Customer
from django.contrib.contenttypes import generic
from django.core import urlresolvers
from core import Core
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
import settings
import os

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class TicketStatus(PersistentModel):
    name = models.CharField(max_length=20)
    order_priority = models.IntegerField()

    class Meta:
        ordering = ['order_priority']

    def __unicode__(self):
        return unicode(self.name)

class TicketPriority(PersistentModel):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.name)

class TicketType(PersistentModel):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.name)

class Ticket(PersistentModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.ForeignKey(TicketStatus)
    priority = models.ForeignKey(TicketPriority)
    type = models.ForeignKey(TicketType)
    spent_time = models.IntegerField(default=0)
    estimated_time = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer)
    assigned_to = models.ForeignKey(User, null=True, blank=True)
    comments = generic.GenericRelation(Comment)
    attachment = models.FileField(upload_to="tickets", storage=fs, null=True)

    def __unicode__(self):
        return unicode(self.title)

    def canBeDeleted(self):
         canBeDeleted = True
         reasons = []

         if self.comments.all().count() > 0:
             canBeDeleted = False
             reasons.append(_("Ticket has comments"))

         if canBeDeleted:
             return (True, "OK")

         return (False, reasons)

    class Meta:
        ordering = ['status', 'date_created']

    def save(self, *args, **kwargs):
        super(Ticket, self).save()

def initial_data():
    TicketStatus.objects.get_or_create(name="Ny", order_priority=1)
    TicketStatus.objects.get_or_create(name="In Progress", order_priority=2)
    TicketStatus.objects.get_or_create(name="Ferdig", order_priority=3)
    TicketStatus.objects.get_or_create(name="Lukket", order_priority=4)

    TicketPriority.objects.get_or_create(name="Lav")
    TicketPriority.objects.get_or_create(name="Normal")
    TicketPriority.objects.get_or_create(name="H&oslash;y")

    TicketType.objects.get_or_create(name="type")
