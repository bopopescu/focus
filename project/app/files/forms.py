# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *

class FileForm(ModelForm):
    class Meta:
        model = File
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'folder')

class FolderForm(ModelForm):
    class Meta:
        model = Folder
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'parent')