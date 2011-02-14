# -*- coding: utf-8 -*-
from django.db import models
from core import Core
from core.models import PersistentModel
from django.core import urlresolvers
from django.utils.translation import ugettext as _

class Announcement(PersistentModel):
    title = models.CharField(_("Title"), max_length=80)
    text = models.TextField(_("Text"))
    attachment = models.FileField(upload_to="uploads/announcements/", verbose_name=_("Attachment"), null=True, blank=True)

    def __unicode__(self):
        return self.title

    def getViewUrl(self):
        return urlresolvers.reverse('app.announcements.views.view', args=("%s" % self.id,))

    def getEditUrl(self):
        return urlresolvers.reverse('app.announcements.views.edit', args=("%s" % self.id,))

    def save(self, *args, **kwargs):

        new = False
        if not self.id:
            new = True

        super(Announcement, self).save()

        #Give the user who created this ALL permissions on object

        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)