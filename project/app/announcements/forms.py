 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets                                       

from models import *

class AnnouncementForm(ModelForm):
    class Meta:
        model = Announcement
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company')