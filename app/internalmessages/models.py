from django.db import models
from django.contrib import admin
from core.models import *
from app.projects.models import *
from app.contacts.models import *    
from reversion.admin import VersionAdmin


class InternalMessage(PersistentModel):
    title = models.CharField("Tittel", max_length=80)
    text = models.TextField()
    
    sender = models.ForeignKey(User, related_name="sendtMessages")
    recipients = models.ManyToManyField(User)
    
    
class internalMessageUser(PersistentModel):
    date_read = models.DateField()
    internalMessage = models.ForeignKey(InternalMessage, related_name="messages")
    recipient = models.ForeignKey(User, related_name="recievedMessages")
    

class InternalMessageAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(InternalMessage, InternalMessageAdmin)