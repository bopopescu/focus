 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from core.widgets import *
from models import *
from django.contrib.auth.decorators import login_required, permission_required

class OrderForm(ModelForm): 
    


    def __init__(self,*args,**kwrds):
        super(OrderForm,self).__init__(*args,**kwrds)
        self.fields['project'].widget = SelectWithPop()
        self.fields['project'].queryset=Project.objects.for_company()
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset=Contact.objects.for_company()
        
        self.fields['responsible'].queryset = get_company_users()
        
    class Meta:
        model = Order
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company')


class OrderFormSimple(ModelForm):
    
    class Meta:
        model = Order
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company','contacts',
                   'participant')