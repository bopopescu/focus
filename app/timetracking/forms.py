 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from models import *
from django.contrib.admin import widgets

from core.widgets import *

class TimetrackingForm(ModelForm):    
    date        = forms.DateField(required=True,input_formats=["%d.%m.%Y"])
    order       = forms.ModelChoiceField(Order.objects.for_company(), widget=SelectWithPop())
    typeOfWork  = forms.ModelChoiceField(TypeOfTimeTracking.objects.for_company(), widget=SelectWithPop())
    
    class Meta:
        model = Timetracking
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company','hours_worked')
        
class TypeOfTimeTrackingForm(ModelForm):
    class Meta:
        model = TypeOfTimeTracking
        exclude = ('deleted', 'date_created', 'date_edited', 'owner','creator','editor','company')