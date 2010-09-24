from django.db import models
from django.contrib import admin
from core.models import *

class Bug(PersistentModel):
    title = models.CharField("Tittel", max_length=80)
    description = models.TextField("Beskrivelse")
    
    def __unicode__(self):
        return self.title
    
import reversion
reversion.register(Bug)