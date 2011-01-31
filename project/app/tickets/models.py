from core.models import PersistentModel, User
from django.db import models
from app.customers.models import Customer
from django.core import urlresolvers


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


    class Meta:
        ordering = ['status', 'date_created']


class Comment(PersistentModel):
    title = models.CharField(max_length=50)
    text = models.TextField()
    Ticket = models.ForeignKey(Ticket)
    

    class Meta:
        ordering = ['date_created']








