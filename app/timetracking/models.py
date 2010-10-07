from django.db import models

from django.contrib import admin
from core.models import PersistentModel
from app.orders.models import *
import datetime

    
class TypeOfTimeTracking(PersistentModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
class Timetracking(PersistentModel):
    
    date = models.DateField()
    order = models.ForeignKey(Order)
    typeOfWork = models.ForeignKey(TypeOfTimeTracking, default=1)
    time_start = models.CharField(max_length=5)
    time_end = models.CharField(max_length=5)
    description = models.TextField()
    
    def __unicode__(self):
        return self.date

class TimetrackingModelAdmin(VersionAdmin):
    """Admin settings go here."""

class TypeOfTimeTrackingModelAdmin(VersionAdmin):
    """Admin settings go here."""

from reversion.admin import VersionAdmin
admin.site.register(TypeOfTimeTracking, TypeOfTimeTrackingModelAdmin)
admin.site.register(Timetracking, TimetrackingModelAdmin)