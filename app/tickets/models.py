from django.db import models
from django.contrib import admin
from core.models import PersistentModel
import datetime

class Ticket(PersistentModel):
    title = models.CharField(max_length=100)
    text = models.TextField()
    
    def __unicode__(self):
        return self.title
    
from reversion.admin import VersionAdmin
class TicketModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Ticket, TicketModelAdmin)