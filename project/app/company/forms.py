# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms
from core.auth.company.models import Company
from core.auth.group.models import Group

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')

    def __init__(self, *args, **kwrds):
        super(CompanyForm, self).__init__(*args, **kwrds)
        self.fields['admin_group'].queryset = Group.objects.filter_current_company()
        self.fields['all_employees_group'].queryset = Group.objects.filter_current_company()

    def clean_MonthsStillValidForEditWhenEditing(self):
        months = int(self.cleaned_data['MonthsStillValidForEditWhenEditing'])

        if months > 0 and months < 13:
            return months

        raise forms.ValidationError("Ugyldig antall måned,velg mellom 1 og 12")

    def clean_DayInMonthsStillValidForEditWhenEditing(self):
        day = int(self.cleaned_data['DayInMonthsStillValidForEditWhenEditing'])

        if day > 0 and day < 15:
            return day

        raise forms.ValidationError("Ugyldig dag,velg mellom 1 og 15")

class newCompanyForm(forms.Form):
    name                = forms.CharField(label="Firmanavn")
    admin_group          = forms.CharField(label="Gruppenavn admin")
    all_employees_group   = forms.CharField(label="Gruppenavn ansatte")

    email_address       = forms.CharField(label="Email address")
    email_host          = forms.CharField(label="Email host")
    email_username      = forms.CharField(label="Email username")
    email_password      = forms.CharField(label="Email password")

    adminuser_name       = forms.CharField(label="Fullt navn admin")
    adminuser_username   = forms.CharField(label="Brukernavn for admin")
    adminuser_password   = forms.CharField(label="Passord for admin")

    def clean_name(self):
       name = self.cleaned_data['name']

       companies = Company.objects.all()

       for i in companies:
           if i.name == name:
               raise forms.ValidationError("Det kreves unikt firmanavn")

       return name
