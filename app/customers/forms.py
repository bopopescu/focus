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
    
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor','company')
    
    def __init__(self,*args,**kwrds):
        super(CustomerForm,self).__init__(*args,**kwrds)
        self.fields['projects'].widget = MultipleSelectWithPop()
        self.fields['projects'].queryset=Project.objects.for_company()
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset=Contact.objects.for_company()
           
class CustomerFormSimple(ModelForm):
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor','company', 'projects')        