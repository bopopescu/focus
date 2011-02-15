# -*- coding: utf-8 -*-
from django.db import models
from core import Core
from django.contrib.contenttypes import generic
from core.models import PersistentModel, Comment
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class Contact(PersistentModel):
    full_name = models.CharField(_("Full name"), max_length=80)
    address = models.CharField(_("Adresse"), max_length=80)
    email = models.EmailField(_("Epostadresse"), max_length=80)
    phone = models.CharField(_("Telefon"), max_length=20)
    comments = generic.GenericRelation(Comment)
    image = models.FileField(upload_to="contacts", storage=fs, null=True, blank=True)

    def __unicode__(self):
        return unicode(self.full_name)

    def canBeDeleted(self):
        return (True, "ok")

    def getImage(self):
        if self.image:
            if os.path.join("/file/", self.image.name):
                return settings.os.path.join("/file/", self.image.name)

        return settings.STATIC_URL + "img/dummy.png"

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.contacts.views.add_ajax')

    @staticmethod
    def simpleform():
        return ContactForm(instance=Contact(), prefix="contacts")

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


from app.contacts.forms import ContactForm