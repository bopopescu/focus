# -*- coding: utf-8 -*-

from django.db import models
from core import Core
from core.models import PersistentModel
from django.core import urlresolvers
from django.utils.translation import ugettext as _

class Contact(PersistentModel):
    full_name = models.CharField(_("Full name"), max_length=80)
    address = models.CharField(_("Adresse"), max_length=80)
    email = models.EmailField(_("Epostadresse"), max_length=80)
    phone = models.CharField(_("Telefon"), max_length=20)

    def __unicode__(self):
        return "%s" % unicode(self.full_name)

    def canBeDeleted(self):
        return (True, "ok")

    def save(self, *args, **kwargs):

        new = False
        if not self.id:
            new = True

        super(Contact, self).save()

        #Give the user who created this ALL permissions on object

        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)
                
            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)

    def getViewUrl(self):
        return urlresolvers.reverse('app.contacts.views.view', args=("%s" % self.id,))

    def getEditUrl(self):
        return urlresolvers.reverse('app.contacts.views.edit', args=("%s" % self.id,))