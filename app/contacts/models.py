# -*- coding: utf-8 -*-

from django.db import models
from core import Core
from core.models import PersistentModel
from django.core import urlresolvers

class Contact(PersistentModel):
    full_name = models.CharField("Fullt navn", max_length=80)
    address = models.CharField("Adresse", max_length=80)
    email = models.EmailField("Epostadresse", max_length=80)
    phone = models.CharField("Telefon", max_length=20)

    def __unicode__(self):
        return "%s" % unicode(self.full_name)

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