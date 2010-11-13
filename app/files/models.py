from django.db import models

from core.models import *

class Folder(PersistentModel):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self', related_name="folders", null=True, default=None, blank=True)

class File(PersistentModel):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="uploads/files/")
    folder = models.ForeignKey(Folder, related_name="files", null=True, default=None, blank=True)
