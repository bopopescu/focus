from core.models import PersistentModel, User
from django.db import models
from app.customers.models import Customer
from django.core import urlresolvers
from core import Core


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
    attachment = models.FileField(upload_to="uploads/tickets")


    def __unicode__(self):
        return unicode(self.title)

    class Meta:
        ordering = ['status', 'date_created']

    def save(self, *args, **kwargs):
        super(Ticket, self).save()

        new = not self.id
        if new:
            current_user = Core.current_user()
            current_user.grant_role("Owner", self)
            admin_group = current_user().get_company_admingroup()
            allemployeesgroup = current_user.get_company_allemployeesgroup()

            if admin_group:
                admin_group.grant_role("Admin", self)
            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)


class Comment(PersistentModel):
    title = models.CharField(max_length=50)
    text = models.TextField()
    Ticket = models.ForeignKey(Ticket, related_name="comments")
    

    class Meta:
        ordering = ['date_created']



def initial_data() :

    TicketStatus.objects.get_or_create(name="Ny", order_priority=1)
    TicketStatus.objects.get_or_create(name="In Progress", order_priority=2)
    TicketStatus.objects.get_or_create(name="Ferdig", order_priority=3)
    TicketStatus.objects.get_or_create(name="Lukket", order_priority=4)

    TicketPriority.objects.get_or_create(name="Lav")
    TicketPriority.objects.get_or_create(name="Normal")
    TicketPriority.objects.get_or_create(name="H&oslash;y")

    TicketType.objects.get_or_create(name="type")










