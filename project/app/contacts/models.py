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
    address = models.CharField(_("Address"), max_length=80)
    email = models.EmailField(_("Email"), max_length=80)
    phone = models.CharField(_("Phone"), max_length=20, default="")
    phone_office = models.CharField(_("Phone office"), max_length=20, default="")
    phone_mobile = models.CharField(_("Mobile phone"), max_length=20, default="")
    description = models.TextField(default="")
    image = models.ImageField(upload_to="contacts", storage=fs, null=True, blank=True)
    comments = generic.GenericRelation(Comment)

    def __unicode__(self):
        return unicode(self.full_name)

    def can_be_deleted(self):
        return (True, "ok")

    def getImage(self):
        if self.image:
            if os.path.join("/file/", self.image.name):
                return os.path.join("/file/", self.image.name)

        return settings.STATIC_URL + "img/person.png"

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

    def get_view_url(self):
        return urlresolvers.reverse('app.contacts.views.view', args=("%s" % self.id,))

    def get_edit_url(self):
        return urlresolvers.reverse('app.contacts.views.edit', args=("%s" % self.id,))


from app.contacts.forms import ContactForm