from django.db import models
from django.contrib import admin
from core.models import *
from app.projects.models import *
from app.contacts.models import *    


class Order(PersistentModel):
    order_name = models.CharField("Ordrenavn", max_length=80)
    
    responsible = models.ForeignKey(User, related_name="ordersWhereResponsible", verbose_name="Ansvarlig")    
    contacts = models.ManyToManyField(Contact, related_name="orders", verbose_name="Kontakter")
    project = models.ForeignKey(Project, related_name="orders", verbose_name="Prosjekt")

    def __unicode__(self):
        return self.order_name
    
class OrderModelAdmin(VersionAdmin):
    """Admin settings go here."""


from reversion.admin import VersionAdmin
admin.site.register(Order, OrderModelAdmin)