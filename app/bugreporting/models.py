from django.db import models
from django.contrib import admin
from core.models import *


class Bug(PersistentModel):
    title = models.CharField("Tittel", max_length=80)
    description = models.TextField("Beskrivelse")
    closed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title

class BugComment(PersistentModel):
    title = models.CharField(max_length=80, blank=True)
    text = models.TextField()
    bug = models.ForeignKey(Bug, related_name="comments")
    
    def __unicode__(self):
        return self.text