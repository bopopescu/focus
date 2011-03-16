# -*- coding: utf-8 -*-
import os
from django.db import models
from core import Core
from core.models import PersistentModel
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class Announcement(PersistentModel):
    title = models.CharField(_("Title"), max_length=80)
    text = models.TextField(_("Text"))
    attachment = models.FileField(upload_to="announcements/", storage=fs, verbose_name=_("Attachment"), null=True,
                                  blank=True)

    def __unicode__(self):
        return self.title

    def getAttachment(self):
        if self.attachment:
            if os.path.join("/file/", self.attachment.name):
                return os.path.join("/file/", self.attachment.name)

        return None

    def getViewUrl(self):
        return urlresolvers.reverse('app.announcements.views.view', args=("%s" % self.id,))

    def getEditUrl(self):
        return urlresolvers.reverse('app.announcements.views.edit', args=("%s" % self.id,))

    def save(self, *args, **kwargs):
        super(Announcement, self).save()