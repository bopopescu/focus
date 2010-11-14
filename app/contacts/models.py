# -*- coding: utf-8 -*-

from django.db import models
from django.contrib import admin
from core.models import PersistentModel

from django.core import urlresolvers


class Contact(PersistentModel):
    full_name = models.CharField("Fullt navn", max_length=80)
    address = models.CharField("Adresse", max_length=80)
    email = models.EmailField("Epostadresse", max_length=80)
    phone = models.CharField("Telefon", max_length=20)
    
    def __unicode__(self):
        return "%s" % unicode(self.full_name)
    
    def getViewUrl(self):
        return urlresolvers.reverse('app.contacts.views.view', args=("%s"%self.id,))

    def getEditUrl(self):
        return urlresolvers.reverse('app.contacts.views.edit', args=("%s"%self.id,))

from reversion.admin import VersionAdmin
class ContactModelAdmin(VersionAdmin):
    """Admin settings go here."""

admin.site.register(Contact, ContactModelAdmin)