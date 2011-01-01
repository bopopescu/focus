# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from core.models import Company, Group

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')

    def __init__(self, *args, **kwrds):
        super(CompanyForm, self).__init__(*args, **kwrds)
        self.fields['adminGroup'].queryset = Group.objects.inCompany()
        self.fields['allEmployeesGroup'].queryset = Group.objects.inCompany()

class newCompanyForm(forms.Form):
    name                = forms.CharField()
    adminGroup          = forms.CharField()
    allEmployeesGroup   = forms.CharField()
    adminuserName       = forms.CharField()
    adminuserUsername   = forms.CharField()
    adminuserPassword   = forms.CharField()