from django.db import models
from core.models import PersistentModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from copy import deepcopy
import os
from django.core import urlresolvers

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class Folder(PersistentModel):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', related_name="folders", null=True, default=None, blank=True)

    def __unicode__(self):
        return self.name


class File(PersistentModel):
    name = models.CharField(max_length=200)
    folder = models.ForeignKey(Folder, related_name="files", null=True, default=None, blank=True)
    file = models.FileField(upload_to="uploaded_files", storage=fs)
    last_revision = models.ForeignKey("File", related_name="revisions", null=True, blank=True)

    def clone(self):
        cloned = deepcopy(self)
        cloned.id = None
        cloned.trash = False
        cloned.deleted = False
        cloned.last_revision = self
        return cloned

    def __unicode__(self):
        return u'%s,%s' % (self.name, self.file.name)

    def get_revisions(self):
        return self.revisions.all().order_by("-date_created")

    def original_name(self):
        list = self.file.name.encode("UTF-8").split("/")
        return list[len(list) - 1]

    def get_file(self):
        if self.file and os.path.join("/file/", self.file.name):
            return os.path.join("/file/", self.file.name)

    def get_edit_url(self):
        return urlresolvers.reverse('app.files.views.edit_file', args=("%s" % self.id,))