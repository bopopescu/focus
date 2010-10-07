 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from models import *
from core.models import *
from core.widgets import *

from app.customers.models import *

class ProjectForm(ModelForm):    
    class Meta:
        model = Project
        fields = ('project_name','customer')
        
    def __init__(self,*args,**kwrds):
        super(ProjectForm,self).__init__(*args,**kwrds)
        self.fields['customer'].widget = SelectWithPop()
        self.fields['customer'].queryset=Customer.objects.for_company()