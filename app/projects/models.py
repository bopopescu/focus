from django.db import models
from django.contrib import admin
from core.models import PersistentModel
from app.customers.models import Customer

class Project(PersistentModel):
    customer = models.ForeignKey(Customer, verbose_name="Kunde", related_name="projects")
    project_name = models.CharField("Prosjektnavn", max_length=80)
    
    def __unicode__(self):
        return self.name

from reversion.admin import VersionAdmin

class ProjectModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Project, ProjectModelAdmin)
