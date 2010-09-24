 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets                                       
from django.forms.formsets import formset_factory
from models import *
from core.models import *

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor','company')
        
class ContactPermissions(ModelForm):
    class Meta:
        model = ObjectPermission  
        exclude = ('content_type', 'object_id')      
    


ContactPermissionFormSet = formset_factory(ContactPermissions, extra=3)
