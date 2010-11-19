 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets                                       
from core.models import *
from django.contrib.auth.models import *

from core.widgets import *


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
class MembershipForm(ModelForm):
    class Meta:
        model = Membership
        fields= ('name','users',)
        
    def __init__(self,*args,**kwrds):
        super(MembershipForm,self).__init__(*args,**kwrds)
        self.fields['users'].widget = MultipleSelectWithPop()
        self.fields['users'].queryset=get_company_users()