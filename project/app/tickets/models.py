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

class TicketPriority(PersistentModel):
    name = models.CharField(max_length=20)

class TicketType(PersistentModel):
    name = models.CharField(max_length=20)


class Ticket(PersistentModel):
    title = models.CharField(max_length=50)
    description = models.TextField()
    status = models.ForeignKey(TicketStatus)
    priority = models.ForeignKey(TicketPriority)
    type = models.ForeignKey(TicketType)
    customer = models.ForeignKey(Customer)
    assigned_to = models.ForeignKey(User, null=True, blank=True)

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








