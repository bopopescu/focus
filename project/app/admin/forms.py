# -*- coding: utf-8 -*-
from core.widgets import *
from django.forms.models import ModelForm
from django import forms
from core.models import User, Group, Company

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email")

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

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'members',)

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

class UserProfileImageForm(ModelForm):
    class Meta:
        model = User
        fields = ('profileImage',)

class UserProfilePasswordForm(forms.Form):
    oldPassword = forms.CharField(label="Gammelt passord", widget=forms.PasswordInput)
    newPassword = forms.CharField(label="Nytt passord", widget=forms.PasswordInput)
    newPasswordCopy = forms.CharField(label="Gjenta nytt passord", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(UserProfilePasswordForm, self).__init__(*args, **kwargs)


    def clean_oldPassword(self):
        oldPass = self.cleaned_data['oldPassword']

        if not self.user.check_password(oldPass):
            raise forms.ValidationError("Feil passord!")

        return oldPass

    def clean_newPassword(self):
        newPass = self.cleaned_data['newPassword']

        if len(newPass) < 5:
            raise forms.ValidationError("Passord må være lenger enn 5 tegn")

        if self.user.check_password(newPass):
            raise forms.ValidationError("Nytt passord må være forskjellig fra det gamle!")

        return newPass

    def clean_newPasswordCopy(self):
        newPass = self.cleaned_data['newPassword']
        newPassCopy = self.cleaned_data['newPasswordCopy']

        if newPass != newPassCopy:
            raise forms.ValidationError("Dette stemmer ikke overens med ditt nye passord, prøv igjen!")

        return newPassCopy