 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from core.widgets import *
from models import *
from django.contrib.auth.decorators import login_required, permission_required

class OrderForm(ModelForm): 
    
    project = forms.ModelChoiceField(Project.objects.for_company(), 
                                     widget=SelectWithPop)
    
    
    contacts = forms.ModelMultipleChoiceField(Contact.objects.for_company(), 
                                              required=False, 
                                              widget=MultipleSelectWithPop)
     
    participants = forms.ModelMultipleChoiceField(get_company_users(), 
                                                  required=False, 
                                                  widget=MultipleSelectWithPop) 
    
    
    def __init__(self,*args,**kwargs):
        super (OrderForm,self ).__init__(*args,**kwargs) # populates the post
        self.fields['responsible'].queryset = get_company_users()
        
    class Meta:
        model = Order
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company')


class OrderFormSimple(ModelForm):
    project         = forms.ModelChoiceField(Project.objects.for_company(), widget=SelectWithPop)
    responsible     = forms.ModelChoiceField(get_company_users())

    class Meta:
        model = Order
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company','contacts',
                   'participant')