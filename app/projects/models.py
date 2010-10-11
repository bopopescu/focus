from django.db import models
from django.contrib import admin
from core.models import PersistentModel
from app.customers.models import Customer
from django.core import urlresolvers

class Project(PersistentModel):
    customer = models.ForeignKey(Customer, verbose_name="Kunde", related_name="projects", default=None, null=True)
    project_name = models.CharField("Prosjektnavn", max_length=80)
    description = models.TextField()
    
    
    def __unicode__(self):
        return self.project_name

    def get_url(self):
        return urlresolvers.reverse('app.projects.views.view', args=("%s"%self.id,))
    
from reversion.admin import VersionAdmin
class ProjectModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Project, ProjectModelAdmin)