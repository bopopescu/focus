# -*- coding: utf-8 -*-
from core import Core
from django.db import models
from core.models import PersistentModel
from django.core import urlresolvers
from django.utils.translation import ugettext as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class Announcement(PersistentModel):
    title = models.CharField(_("Title"), max_length=80)
    text = models.TextField(_("Text"))
    attachment = models.FileField(upload_to="announcements/", storage=fs, verbose_name=_("Attachment"), null=True,
                                  blank=True)

    def __unicode__(self):
        return self.title

    def get_attachment(self):
        if self.attachment:
            if os.path.join("/file/", self.attachment.name):
                return os.path.join("/file/", self.attachment.name)

        return None

    def get_view_url(self):
        return urlresolvers.reverse('app.announcements.views.view', args=("%s" % self.id,))

    def get_edit_url(self):
        return urlresolvers.reverse('app.announcements.views.edit', args=("%s" % self.id,))

    def save(self, *args, **kwargs):
        super(Announcement, self).save()