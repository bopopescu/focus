 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from models import *
from core.models import *

class ProjectForm(ModelForm):    
    class Meta:
        model = Project
        fields = ('project_name',)