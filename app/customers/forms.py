 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.conf import settings

from django.contrib.admin import widgets                                       
from models import *
from app.projects.models import Project
from app.contacts.models import Contact
from django.utils.safestring import mark_safe

from core.widgets import *

class CustomerForm(ModelForm):
    projects = forms.ModelMultipleChoiceField(Project.objects.for_company(), required=False, widget=MultipleSelectWithPop) 
    contacts = forms.ModelMultipleChoiceField(Contact.objects.for_company(), required=False, widget=MultipleSelectWithPop) 

    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor','company')
        
class CustomerFormSimple(ModelForm):
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor','company', 'projects')        