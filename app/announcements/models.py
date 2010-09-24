from django.db import models
from django.contrib import admin
from core.models import *


class Announcement(PersistentModel):
    title = models.CharField("Overskrift", max_length=80)
    text = models.TextField("Tekst")

    def __unicode__(self):
        return self.title
    
import reversion
reversion.register(Announcement)