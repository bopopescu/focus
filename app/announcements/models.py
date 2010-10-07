from django.db import models
from django.contrib import admin

from core.models import PersistentModel

class Announcement(PersistentModel):
    title = models.CharField("Overskrift", max_length=80)
    text = models.TextField("Tekst")

    def __unicode__(self):
        return self.title
    
from reversion.admin import VersionAdmin
class ModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Announcement, ModelAdmin)