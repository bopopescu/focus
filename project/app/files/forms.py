# -*- coding: utf-8 -*-
from django import forms
from models import *

class FileForm(forms.ModelForm):
    tags = forms.CharField(max_length=200)
    class Meta:
        model = File
        fields = ('name', 'file','tags')


class FileTagForm(forms.ModelForm):
    class Meta:
        model = FileTag
        fields = ('name',)