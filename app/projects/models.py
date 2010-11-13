from django.db import models
from django.contrib import admin
from core.models import PersistentModel
from app.customers.models import Customer
from django.core import urlresolvers
from django.contrib.auth.models import User

class Project(PersistentModel):
    pid = models.IntegerField("Prosjektnr", null=True)
    customer = models.ForeignKey(Customer, verbose_name="Kunde", related_name="projects", default=None, null=True)
    project_name = models.CharField("Prosjektnavn", max_length=80)
    description = models.TextField()
    deliveryAddress = models.CharField(max_length=150, null=True)
    responsible = models.ForeignKey(User, related_name="projectsWhereResponsible", verbose_name="Ansvarlig", null=True)
    deliveryDate = models.DateField(verbose_name="Leveringsdato", null=True, blank=True)
    deliveryDateDeadline = models.DateField(verbose_name="Leveringsfrist", null=True, blank=True)


    def __unicode__(self):
        return self.project_name

    def get_url(self):
        return urlresolvers.reverse('app.projects.views.view', args=("%s" % self.id,))


class ProjectFolder(PersistentModel):
    project_id = models.ForeignKey(Project, related_name="folders")
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return "Prosjektmappe: %s" % self.name

class ProjectFile(PersistentModel):
    project_id = models.ForeignKey(Project, related_name="files")
    name = models.CharField(max_length=100)
    folder = models.ForeignKey(ProjectFolder, related_name="files")

    def __unicode__(self):
        return "Prosjektfil: %s" % self.name

from reversion.admin import VersionAdmin

class ProjectModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Project, ProjectModelAdmin)