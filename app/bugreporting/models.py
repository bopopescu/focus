from django.db import models
from django.contrib import admin
from core.models import *

class Bug(PersistentModel):
    title = models.CharField("Tittel", max_length=80)
    description = models.TextField("Beskrivelse")
    closed = models.BooleanField(default=False)
    image = models.FileField(upload_to='../uploads/')
    
    def __unicode__(self):
        return self.title

class BugComment(PersistentModel):
    text = models.TextField()
    bug = models.ForeignKey(Bug, related_name="comments")

from reversion.admin import VersionAdmin
class ModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Bug, ModelAdmin)
admin.site.register(BugComment, ModelAdmin)