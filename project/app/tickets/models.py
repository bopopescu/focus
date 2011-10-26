# -*- coding: utf-8 -*-
from datetime import datetime
from app.projects.models import Milestone
from app.tickets.utils import send_assigned_mail, send_update_mails
from core import Core
from core.auth.company.models import Company
from core.auth.user.models import User
from core.cache import cachedecorator
from django.db import models
from django.core.cache import cache
from app.customers.models import Customer
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.core import urlresolvers
from core.managers import PersistentManager
import settings
import os

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class TicketBase(models.Model):
    """ Used as base class by Ticket and TicketUpdate instead of PersistentModel
        Objects can be created be client users
    """
    company = models.ForeignKey(Company, default=None, null=True)
    client_user = models.ForeignKey('client.ClientUser', blank=True, null=True, default=None,
                                    related_name='client_tickets')
    user = models.ForeignKey(User, blank=True, null=True, default=None, related_name='tickets')
    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True)
    trashed = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    def save(self, **kwargs):
        action = 'EDIT'
        if not self.id:
            action = 'ADD'

        super(TicketBase, self).save()

        if Core.current_user():

            if action == "ADD":
                Core.current_user().grant_role("Admin", self)
                admin_group = Core.current_user().get_company_admingroup()
                allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

                if admin_group:
                    admin_group.grant_role("Admin", self)

                if allemployeesgroup:
                    allemployeesgroup.grant_role("Member", self)

            if self.user:
                self.user.grant_role('Admin', self)

    def trash(self):
        self.trashed = True
        self.save()

    @property
    @cachedecorator('creator')
    def creator(self):
        creator = self.client_user or self.user
        return creator

class TicketStatus(models.Model):
    name = models.CharField(max_length=20)
    order_priority = models.IntegerField()

    class Meta:
        ordering = ['order_priority']

    def __unicode__(self):
        return unicode(self.name)


class TicketPriority(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.name)


class TicketType(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(default=None, blank=True, null=True)
    company = models.ForeignKey(Company, null=True, default=None)

    def __unicode__(self):
        return unicode(self.name)

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.tickets.views.add_ticket_type_ajax')

    @staticmethod
    def simpleform():
        from app.tickets.forms import AddTicketTypeForm
        return AddTicketTypeForm(instance=TicketType(), prefix="ticket_type")

class Ticket(TicketBase):
    title = models.CharField(_("Title"), max_length=50)
    description = models.TextField(_("Description"), )
    status = models.ForeignKey(TicketStatus, verbose_name=_("Status"), default=1)
    priority = models.ForeignKey(TicketPriority, verbose_name=_("Priority"), default=2)
    type = models.ForeignKey(TicketType, verbose_name=_("Category"))
    spent_time = models.IntegerField(_("Spent time"), default=0)
    estimated_time = models.IntegerField(_("Estimated time"), default=0)
    due_date = models.DateTimeField(null=True, blank=True, default=None)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), null=True, blank=True)
    order = models.ForeignKey('orders.Order', null=True, blank=True, verbose_name=_("Order"),
                              related_name="tickets")
    assigned_to = models.ForeignKey(User, null=True, blank=True, verbose_name=_("Assigned to"),
                                    related_name="assigned_tickets")
    #mail_excluded = models.ManyToManyField(User, null=True, blank=True)
    attachment = models.FileField(upload_to="tickets", storage=fs, null=True, verbose_name=_("Attachment"))
    milestone = models.ForeignKey(Milestone, blank=True, null=True, verbose_name=_('milestone'))
    visited_by_since_last_edit = models.ManyToManyField(User)

    objects = PersistentManager()
    all_objects = models.Manager()

    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ['status', 'date_created']


    def invalidate_cache(self):
      cache.delete("cachedecorator_%s_%s_%s" % (self.__class__.__name__, self.pk, "get_clients"))
      cache.delete("cachedecorator_%s_%s_%s" % (self.__class__.__name__, self.pk, "get_updates"))
      cache.delete("cachedecorator_%s_%s_%s" % (self.__class__.__name__, self.pk, "get_priority"))
      cache.delete("cachedecorator_%s_%s_%s" % (self.__class__.__name__, self.pk, "get_status"))

    @cachedecorator('get_clients')
    def get_clients(self):
        return list(self.clients.all().select_related())

    @cachedecorator('get_updates')
    def get_updates(self):
        return list(self.updates.all().select_related())

    @cachedecorator('get_priority')
    def get_priority(self):

        result = ""
        if self.priority.name == ("Low"):
            result = "gray"

        elif self.priority.name == ("Medium"):
            result = "blue"

        elif self.priority.name == ("High"):
            result =  "red"

        elif self.priority.name == ("standard"):
            result =  "gray"

        return {'color':result, 'name':self.priority.name}

    @cachedecorator('get_status')
    def get_status(self):

        result = "red"

        if self.status.name == ("New"):
            result = "green"

        elif self.status.name == ("In Progress"):
            result = "blue"

        elif self.status.name == ("Need feedback"):
            result = "red"

        elif self.status.name == ("Closed"):
            result =  "gray"

        elif self.status.name == ("standard"):
            result =  "gray"

        return {'color':result, 'name': self.status.name}

    def add_user_to_visited_by_since_last_edit(self, user):
        if user not in self.visited_by_since_last_edit.all():
            self.visited_by_since_last_edit.add(user)

    @cachedecorator('mark_as_unread_for_current_user')
    def mark_as_unread_for_current_user(self):
        return Core.current_user() in self.get_recipients() and not Core.current_user() in self.visited_by_since_last_edit.all()

    def get_recipients(self):
        """
        Return list of users who have commented or created this ticket
        """
        recipients = set([])

        if self.user:
            recipients.add(self.user)

        if self.assigned_to:
            recipients.add(self.assigned_to)

        for update in self.updates.all():
            if update.user:
                recipients.add(update.creator)

        return recipients

    def get_view_url(self):
        return urlresolvers.reverse('app.tickets.views.view', args=("%s" % self.id,))

    def get_update_url(self):
        return urlresolvers.reverse('app.tickets.views.edit', args=("%s" % self.id,))

    def save(self, **kwargs):
        if 'update' in kwargs:
            send_update_mails(self, kwargs['update'])
        action = 'EDIT'
        if not self.id:
            action = 'ADD'

        if self.id:
            self.visited_by_since_last_edit = []
            if Core.current_user():
                self.visited_by_since_last_edit.add(Core.current_user())

        super(Ticket, self).save()

        if action == 'ADD':
            if self.assigned_to:
                send_assigned_mail(self.assigned_to, self, assigned=True)
            if self.company:
                if self.company.admin_group:
                    self.company.admin_group.grant_role('Admin', self)
                if self.company.all_employees_group:
                    self.company.all_employees_group.grant_role('Member', self)

        
        self.invalidate_cache()

    def check_assigned_to(self):
        try:
            old = Ticket.objects.get(id=self.id).assigned_to
        except Ticket.DoesNotExist:
            old = False

        if not old == self.assigned_to:
            if self.assigned_to:
                send_assigned_mail(self.assigned_to, self)
            if old:
                send_assigned_mail(old, self, assigned=False)


    def set_user(self, user):
        self.user = user
        self.company = user.get_company()


    def can_be_deleted(self):
        can_be_deleted = True
        reasons = []

        if self.updates.all().count() > 0:
            can_be_deleted = False
            reasons.append(_("Ticket has comments"))

        if can_be_deleted:
            return True, "OK"

        return False, reasons

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
        'customer_id': (Customer, 'name',),
        'assigned_to_id': (User, 'username')
    }

    def create_model_dict(self):
        data = {}
        ignore_list = ('date_edited', )

        for field in self._meta.fields:
            if field.attname.startswith('_') or field.attname in ignore_list:
                continue

            field_value = getattr(self, field.attname)

            if field.attname in self.foreign_key_dict:
                #Check if foreign-key value is None
                if field_value is None:
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


class TicketUpdate(TicketBase):
    ticket = models.ForeignKey(Ticket, related_name="updates")
    comment = models.TextField()
    attachment = models.FileField(upload_to="tickets/comments", storage=fs, null=True)
    public = models.BooleanField(default=False, blank=True)

    objects = PersistentManager()
    all_objects = models.Manager()

    @cachedecorator('get_attachment_url')
    def get_attachment_url(self):
        if self.attachment:
            return os.path.join("/file/", self.attachment.name)
        return None

    def get_view_url(self):
        return urlresolvers.reverse('app.tickets.views.view', args=("%s" % self.ticket.id,))

    @cachedecorator('get_attachment_name')
    def get_attachment_name(self):
        return self.attachment.name.split(os.sep)[-1]

    def create_update_lines(self, differences):
        for diff in differences:
            change_text = ("%s %s %s %s %s") %\
                          (diff, _("changed from"), differences[diff][1], _("to"), differences[diff][0])
            TicketUpdateLine.objects.create(update=self, change=change_text)

    @cachedecorator('get_attachment')
    def get_attachment(self):
        if self.attachment:
            return os.path.join("/file/", self.attachment.name)
        return None

    @cachedecorator('get_update_lines')
    def get_update_lines(self):
        return list(self.update_lines.all().select_related())

    def __unicode__(self):
        return u"Comment for ticket %s, by %s %s" % (self.ticket, self.user, self.date_created.strftime("%d.%m.%Y"))


class TicketUpdateLine(TicketBase):
    update = models.ForeignKey(TicketUpdate, related_name='update_lines')
    change = models.CharField(max_length=250)


def initial_data():
    TicketStatus.objects.get_or_create(name=_("New"), order_priority=1)
    TicketStatus.objects.get_or_create(name=_("In Progress"), order_priority=2)
    TicketStatus.objects.get_or_create(name=_("Need feedback"), order_priority=3)
    TicketStatus.objects.get_or_create(name=_("Closed"), order_priority=4)

    TicketPriority.objects.get_or_create(name=_("Low"))
    TicketPriority.objects.get_or_create(name=_("Medium"))
    TicketPriority.objects.get_or_create(name=_("High"))

    TicketType.objects.get_or_create(name="type")