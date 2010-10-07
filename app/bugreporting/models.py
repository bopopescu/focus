from django.db import models
from django.contrib import admin
from core.models import PersistentModel


class Bug(PersistentModel):
    title = models.CharField("Tittel", max_length=80)
    description = models.TextField("Beskrivelse")
    closed = models.BooleanField(default=False)
    
    image = models.FileField(upload_to="uploads/bugreporting/", verbose_name="Bilde")
    
    def __unicode__(self):
        return self.title

class BugComment(PersistentModel):
    title = models.CharField(max_length=80, blank=True)
    text = models.TextField()
    bug = models.ForeignKey(Bug, related_name="comments")
    
    image = models.FileField(upload_to="uploads/bugcomments/", verbose_name="Bilde")

    def __unicode__(self):
        return self.text