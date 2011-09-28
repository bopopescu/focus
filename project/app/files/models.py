from django.db import models
from core.models import PersistentModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from copy import deepcopy
import os
from django.core import urlresolvers
from core.templatetags.thumbnail import thumbnail_with_max_side
from django.utils.translation import ugettext as _

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class Folder(PersistentModel):
    name = models.CharField(_("Name"), max_length=150)
    parent = models.ForeignKey('self', related_name="folders", verbose_name=_("Parent"), null=True, default=None,
                               blank=True)

    def __unicode__(self):
        return self.name


class FileTag(PersistentModel):
    name = models.CharField(_("Name"), max_length=50)

    def __unicode__(self):
        return self.name


class File(PersistentModel):
    name = models.CharField(_("Name"), max_length=200)
    folder = models.ForeignKey(Folder, related_name="files", verbose_name=_("Folder"), null=True, default=None,
                               blank=True)
    file = models.FileField(upload_to="uploaded_files", verbose_name=_("File"), storage=fs)
    parent_file = models.ForeignKey("File", related_name="revisions", verbose_name=_("Parent file"), null=True,
                                    blank=True)
    tags = models.ManyToManyField(FileTag, related_name="files", verbose_name=_("Tags"))

    def clone(self):
        copied_file = deepcopy(self)
        copied_file.id = None
        copied_file.trashed = True
        copied_file.parent_file = self

        return copied_file

    def recover(self):
        clone = self.parent_file.clone()
        clone.save()

        self.parent_file.name = self.name
        self.parent_file.file = self.file
        self.parent_file.save()

    def __unicode__(self):
        return u'%s,%s' % (self.name, self.file.name)

    def get_file_extension(self):
        basename, file_extension = os.path.splitext(self.file.name)
        return file_extension

    def get_file_icon(self):
        file_extension = self.get_file_extension()

        path = settings.STATIC_URL + "img/icons/extensions/page_"

        if file_extension == ".pdf":
            return path + "pdf.png"
        elif file_extension == ".xls" or file_extension == ".xlsx":
            return path + "excel.png"
        elif file_extension == ".zip" or file_extension == ".gzip":
            return path + "zip.png"
        elif file_extension == ".odt" or file_extension == ".doc" or file_extension == ".docx":
            return path + "word.png"
        elif file_extension == ".jpg" or file_extension == ".png" or file_extension == ".gif":
            try:
                return thumbnail_with_max_side(self.file, "25")
            except Exception:
                return path + "unknown.png"
        else:
            return path + "unknown.png"


    def get_revisions(self):
        if self.id:
            return self.revisions.all().order_by("-date_created")
        return []

    def original_name(self):
        list = self.file.name.encode("UTF-8").split("/")
        return list[len(list) - 1]

    def get_file(self):
        if self.file and os.path.join("/file/", self.file.name):
            return os.path.join("/file/", self.file.name)

    def get_edit_url(self):
        return urlresolvers.reverse('app.files.views.edit_file', args=("%s" % self.id,))

    def get_recover_url(self):
        return urlresolvers.reverse('app.files.views.recover', args=("%s" % self.id,))