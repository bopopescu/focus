 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets                                       

from models import *

class BugreportingForm(ModelForm):
    class Meta:
        model = Bug
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company',)
        
class CommentForm(ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols':'30;','rows':'5',}))
    class Meta:
        model = BugComment
        fields = ('text',)