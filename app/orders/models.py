from django.db import models
from django.contrib import admin
from core.models import *
from app.projects.models import *
from app.contacts.models import *    
from django.core import urlresolvers


STATE_CHOICES = (
    ('T', 'Tilbud'),
    ('O', 'Ordre'),
    ('F', 'Til fakturering'),
    ('A', 'Arkivert'),
)

class Order(PersistentModel):

    oid                     = models.IntegerField("Ordrenr", null=True, blank=True)
    order_name              = models.CharField("Navn", max_length=80)
    customer                = models.ForeignKey(Customer, related_name="orders", verbose_name="Kunde", blank=True, null=True)
    project                 = models.ForeignKey(Project, related_name="orders", verbose_name="Prosjekt", blank=True, null=True)
    responsible             = models.ForeignKey(User, related_name="ordersWhereResponsible", verbose_name="Ansvarlig")

    delivery_date           = models.DateField(verbose_name="Leveringsdato", null=True, blank=True)
    delivery_date_deadline  = models.DateField(verbose_name="Leveringsfrist", null=True, blank=True)

    description             = models.TextField("Beskrivelse")

    contacts                = models.ManyToManyField(Contact, related_name="orders", verbose_name="Kontakter", blank=True)

    state                   = models.CharField(max_length=1, choices = STATE_CHOICES)

    def __unicode__(self):
        return self.order_name
    
    def get_url(self):
        return urlresolvers.reverse('app.orders.views.edit', args=("%s"%self.id,))




class Task(PersistentModel):
    order = models.ForeignKey(Order, related_name="tasks")
    text  = models.TextField("Oppgave")

    def __unicode__(self):
        return self.text


class OrderModelAdmin(VersionAdmin):
    """Admin settings go here."""


from reversion.admin import VersionAdmin
admin.site.register(Order, OrderModelAdmin)