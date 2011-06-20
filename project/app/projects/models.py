# -*- coding: utf-8 -*-
from django.db import models
from app.contacts.models import Contact
from app.files.models import File
from core import Core
from django.contrib.contenttypes import generic
from core.models import PersistentModel, User, Comment
from app.customers.models import Customer
from django.core import urlresolvers
from datetime import timedelta, datetime
import time
from django.utils.translation import ugettext as _
from django.db.models import Max

class Project(PersistentModel):
    pid = models.IntegerField(_("Project number"), null=True)
    POnumber = models.CharField(_("PO-number"), max_length=150, blank=True, null=True)
    customer = models.ForeignKey(Customer, verbose_name=_("Customer"), related_name="projects", default=None, null=True)
    project_name = models.CharField(_("Name"), max_length=80)
    description = models.TextField()
    deliveryAddress = models.TextField(_("Delivery address"), max_length=150, null=True)
    deliveryDate = models.DateTimeField(verbose_name=_("Delivery date"), null=True, blank=True)
    deliveryDateDeadline = models.DateTimeField(verbose_name=_("Delivery deadline"), null=True, blank=True)
    responsible = models.ForeignKey(User, related_name="projectsWhereResponsible", verbose_name=_("Responsible"),                                null=True)
    contact = models.ForeignKey(Contact, related_name="projects", null=True)
    files = models.ManyToManyField(File)
    comments = generic.GenericRelation(Comment)

    def __unicode__(self):
        return self.project_name

    @staticmethod
    def calculate_next_pid():
        projects = Project.objects.filter_current_company()
        max_pid = (projects.aggregate(Max("pid"))['pid__max'])
        if max_pid:
            return max_pid+1
        return 1
    
    def can_be_deleted(self):
        can_be_deleted = True
        reasons = []

        if self.orders.all().count() > 0:
            can_be_deleted = False
            reasons.append(_("Project has active orders"))

        if can_be_deleted:
            return (True, "OK")

        return (False, reasons)

    def get_view_url(self):
        return urlresolvers.reverse('app.projects.views.view', args=("%s" % self.id,))

    def percentDone(self):
        if self.date_created and self.deliveryDate:
            realDiff = (time.mktime(datetime.now().timetuple()) - time.mktime(self.date_created.timetuple()))
            estimatedDiff = (time.mktime(self.deliveryDate.timetuple()) - time.mktime(self.date_created.timetuple()))

            if realDiff > estimatedDiff:
                return 100

            return (realDiff / estimatedDiff) * 100

        return 0

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.projects.views.project_ajax.add')

    @staticmethod
    def simpleform():
        return ProjectFormSimple(instance=Project(), prefix="projects")

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(Project, self).save()

        #Give the user who created this ALL permissions on object
        if new:
            Core.current_user().grant_role("Owner", self)
            admin_group = Core.current_user().get_company_admingroup()

            if admin_group:
                admin_group.grant_role("Admin", self)

class Milestone(PersistentModel):
    project = models.ForeignKey(Project, related_name="milestones")
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __unicode__(self):
        return "Milestone %s for project %s" % (self.name, self.project)

from app.projects.forms import ProjectFormSimple