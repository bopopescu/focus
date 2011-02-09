# -*- coding: utf-8 -*-
from core.widgets import *
from django.forms.models import ModelForm
from core.models import User, Group, Company

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("first_name","last_name","email")

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('profileImage',)
        
class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'members',)

    def __init__(self, *args, **kwrds):
        super(GroupForm, self).__init__(*args, **kwrds)
        self.fields['members'].widget = MultipleSelectWithPop()
        self.fields['members'].queryset = User.objects.inCompany()


class HourRegistrationManuallyForm(ModelForm):
    class Meta:
        model = User
        fields = ('validEditHourRegistrationsToDate', 'validEditHourRegistrationsFromDate',)
           
    def __init__(self, *args, **kwargs):
        super(HourRegistrationManuallyForm, self).__init__(*args, **kwargs)
        self.fields['validEditHourRegistrationsToDate'].required = False
        self.fields['validEditHourRegistrationsToDate'].widget = DatePickerField(format="%d.%m.%Y")
        self.fields['validEditHourRegistrationsToDate'].input_formats = ["%d.%m.%Y"]
        self.fields['validEditHourRegistrationsFromDate'].required = False
        self.fields['validEditHourRegistrationsFromDate'].widget = DatePickerField(format="%d.%m.%Y")
        self.fields['validEditHourRegistrationsFromDate'].input_formats = ["%d.%m.%Y"]