 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from models import *
from core.models import *
from core.widgets import *

from app.customers.models import *

class ProjectForm(ModelForm):

    deliveryDate = forms.DateField(required=True, input_formats=["%d.%m.%Y"], widget=DatePickerField(format="%d.%m.%Y"))
    deliveryDateDeadline = forms.DateField(required=True, input_formats=["%d.%m.%Y"], widget=DatePickerField(format="%d.%m.%Y"))

    class Meta:
        model = Project
        fields = ('pid','project_name','customer','description','deliveryAddress','responsible','deliveryDate','deliveryDateDeadline',)
        
    def __init__(self,*args,**kwrds):
        super(ProjectForm,self).__init__(*args,**kwrds)
        self.fields['customer'].widget = SelectWithPop()
        self.fields['customer'].queryset=Customer.objects.for_company()
        self.fields['responsible'].queryset = get_company_users()