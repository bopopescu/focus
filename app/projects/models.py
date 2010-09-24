from django.db import models
from django.contrib import admin
from core.models import *

class Project(PersistentModel):
    project_name = models.CharField("Prosjektnavn", max_length=80)
    
    def __unicode__(self):
        return self.project_name

from reversion.admin import VersionAdmin

class ProjectModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Project, ProjectModelAdmin)
