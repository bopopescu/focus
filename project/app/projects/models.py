# -*- coding: utf-8 -*-
from django.db import models
from core import Core
from core.models import PersistentModel, User
from app.customers.models import Customer
from django.core import urlresolvers
from datetime import timedelta, datetime
import time

class Project(PersistentModel):
    pid = models.IntegerField("Prosjektnr", null=True)
    POnumber = models.CharField("PO-number", max_length=150, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name="Kunde", related_name="projects", default=None, null=True)
    project_name = models.CharField("Prosjektnavn", max_length=80)
    description = models.TextField()
    deliveryAddress = models.CharField(max_length=150, null=True)
    responsible = models.ForeignKey(User, related_name="projectsWhereResponsible", verbose_name="Ansvarlig", null=True)
    deliveryDate = models.DateTimeField(verbose_name="Leveringsdato", null=True, blank=True)
    deliveryDateDeadline = models.DateTimeField(verbose_name="Leveringsfrist", null=True, blank=True)

    def __unicode__(self):
        return self.project_name

    def getViewUrl(self):
        return urlresolvers.reverse('app.projects.views.view', args=("%s" % self.id,))

    def percentDone(self):
        realDiff = (time.mktime(datetime.now().timetuple()) - time.mktime(self.date_created.timetuple()))
        estimatedDiff = (time.mktime(self.deliveryDate.timetuple()) - time.mktime(self.date_created.timetuple()))

        if realDiff > estimatedDiff:
            return 100

        return (realDiff / estimatedDiff) * 100

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.projects.views.add_ajax')

    @staticmethod
    def simpleform():
        return ProjectFormSimple(instance=Project())

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Project, self).save()

        #Give the user who created this ALL permissions on object
        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

class Milestone(PersistentModel):
    project = models.ForeignKey(Project, related_name="milestones")
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __unicode__(self):
        return "Milestone %s for project %s" % (self.name, self.project)

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


from app.projects.forms import ProjectFormSimple
