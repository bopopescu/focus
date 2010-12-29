# -*- coding: utf-8 -*-
from core.shortcuts import get_company_users
from core.widgets import *
from django.forms.models import ModelForm
from core.models import User, Group

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'canLogin', 'profileImage',)

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('profileImage',)

class MembershipForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'users',)

    def __init__(self, *args, **kwrds):
        super(MembershipForm, self).__init__(*args, **kwrds)
        self.fields['users'].widget = MultipleSelectWithPop()
        self.fields['users'].queryset = get_company_users()