# -*- coding: utf-8 -*-
from core.models import PersistentModel, Comment
from core.auth.user.models import User
from django.db import models
from app.customers.models import Customer
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
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"), )
    status = models.ForeignKey(TicketStatus, verbose_name=_("Status"))
    priority = models.ForeignKey(TicketPriority, verbose_name=_("Priority"))
    type = models.ForeignKey(TicketType, verbose_name=_("Type"))
    spent_time = models.IntegerField(_("Spent time"), default=0)
    estimated_time = models.IntegerField(_("Estimated time"), default=0)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"))
    order = models.ForeignKey('orders.Order', null=True, blank=True, verbose_name=_("Order"), related_name="tickets")
    assigned_to = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Assigned to"))
    attachment = models.FileField(upload_to="tickets", storage=fs, null=True, verbose_name=_("Attachment"))

    def __unicode__(self):
        return unicode(self.title)


    class Meta:
        ordering = ['status', 'date_created']

    def can_be_deleted(self):
        can_be_deleted = True
        reasons = []

        if self.updates.all().count() > 0:
            can_be_deleted = False
            reasons.append(_("Ticket has comments"))

        if can_be_deleted:
            return (True, "OK")

        return (False, reasons)

    def get_attachment_url(self):
        if self.attachment:
            return os.path.join("/file/", self.attachment.name)
        return None

    def get_attachment_name(self):
        return self.attachment.name.split(os.sep)[-1]

    foreign_key_dict = {
        'status_id': (TicketStatus, 'name',),
        'priority_id': (TicketPriority, 'name',),
        'type_id': (TicketType, 'name',),
        'customer_id': (Customer, 'full_name',),
        'assigned_to_id': (User, 'username')
    }

    def create_model_dict(self):
        data = {}
        ignore_list = ('_state', 'date_edited')

        for field in self._meta.fields:
            if field.attname.startswith('_') or field.attname in ignore_list:
                continue

            field_value = getattr(self, field.attname)

            if field.attname in self.foreign_key_dict:

                #Check if foreign-key value is None
                if field_value == None:
                    data[field.verbose_name] = None
                    continue

                model_class = self.foreign_key_dict[field.attname][0]
                model_attr = self.foreign_key_dict[field.attname][1]
                id = field_value
                field_value = getattr(model_class.objects.get(id=id), model_attr)

            data[field.verbose_name] = field_value

        return data

    @staticmethod
    def find_differences(ticket1, ticket2):
        ticket1 = ticket1.create_model_dict()
        ticket2 = ticket2.create_model_dict()
        diff = {}
        for field in ticket1:
            try:
                if ticket1[field] != ticket2[field]:
                    diff[field] = (ticket1[field], ticket2[field],)
            except KeyError:
                pass

        return diff

class TicketUpdate(PersistentModel):
    ticket = models.ForeignKey(Ticket, related_name="updates")
    comment = models.TextField()
    attachment = models.FileField(upload_to="tickets/comments", storage=fs, null=True)
    
    def get_attachment_url(self):
        if self.attachment:
            return os.path.join("/file/", self.attachment.name)
        return None

    def get_attachment_name(self):
        return self.attachment.name.split(os.sep)[-1]

    def create_update_lines(self, differences):
        for diff in differences:
            change_text = _("%s changed from %s to %s") %\
                          (diff, differences[diff][1], differences[diff][0])
            TicketUpdateLine.objects.create(update=self, change=change_text)

    def get_attachment(self):
        if self.attachment:
            return os.path.join("/file/", self.attachment.name)
        return None

class TicketUpdateLine(PersistentModel):
    update = models.ForeignKey(TicketUpdate, related_name='update_lines')
    change = models.CharField(max_length=250)


def initial_data():
    TicketStatus.objects.get_or_create(name=_("New"), order_priority=1)
    TicketStatus.objects.get_or_create(name=_("In Progress"), order_priority=2)
    TicketStatus.objects.get_or_create(name=_("Completed"), order_priority=3)
    TicketStatus.objects.get_or_create(name=_("Closed"), order_priority=4)

    TicketPriority.objects.get_or_create(name=_("Low"))
    TicketPriority.objects.get_or_create(name=_("Medium"))
    TicketPriority.objects.get_or_create(name=_("High"))

    TicketType.objects.get_or_create(name="type")