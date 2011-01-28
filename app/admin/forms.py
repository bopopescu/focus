# -*- coding: utf-8 -*-
from core.shortcuts import get_company_users
from core.widgets import *
from django.forms.models import ModelForm
from core.models import User, Group, Company

class UserForm(ModelForm):
    class Meta:
        model = User

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