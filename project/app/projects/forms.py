# -*- coding: utf-8 -*-
from django.forms import ModelForm
import django.forms as forms
from models import *
from core.widgets import SelectWithPop, DatePickerField
from django.utils.translation import ugettext as _

class ProjectForm(ModelForm):
    deliveryDate = forms.DateField(required=True, input_formats=["%d.%m.%Y"], widget=DatePickerField(format="%d.%m.%Y"))
    deliveryDateDeadline = forms.DateField(required=True, input_formats=["%d.%m.%Y"],
                                           widget=DatePickerField(format="%d.%m.%Y"))

    class Meta:
        model = Project
        fields = ('pid', 'project_name', 'customer', 'description', 'deliveryAddress', 'responsible', 'deliveryDate',
                  'deliveryDateDeadline',)

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget = SelectWithPop(Customer)
        self.fields['customer'].queryset = Customer.objects.inCompany()
        self.fields['responsible'].queryset = User.objects.inCompany()

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_pid(self):
        pid = self.cleaned_data['pid']

        projects = Project.objects.inCompany()
        for i in projects:
            if self.id == i.id:
                continue

            if i.pid == pid:
                raise forms.ValidationError("Det kreves unikt prosjektnr")

        return pid

class ProjectFormSimple(ModelForm):

    class Meta:
        model = Project
        fields = ('pid', 'project_name', 'customer', 'description', 'deliveryAddress', 'responsible')

    def __init__(self, *args, **kwargs):
        super(ProjectFormSimple, self).__init__(*args, **kwargs)
        self.fields['customer'].queryset = Customer.objects.inCompany()
        self.fields['responsible'].queryset = User.objects.inCompany()

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_pid(self):
        pid = self.cleaned_data['pid']

        projects = Project.objects.inCompany()
        for i in projects:
            if self.id == i.id:
                continue

            if i.pid == pid:
                raise forms.ValidationError("Det kreves unikt prosjektnr")

        return pid


