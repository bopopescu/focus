# -*- coding: utf-8 -*-
from django.forms import ModelForm
import django.forms as forms
from app.customers.models import Customer
from app.projects.models import Milestone
from core.auth.user.models import User
from models import Project
from core.widgets import SelectWithPop, DatePickerField
from django.utils.translation import ugettext as _

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('pid', 'project_name', 'customer', 'responsible', 'deliveryAddress', 'deliveryDate',
                  'deliveryDateDeadline', 'description',)

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields['deliveryDate'].widget = DatePickerField(format="%d.%m.%Y",)
        self.fields['deliveryDate'].input_formats = ["%d.%m.%Y"]
        self.fields['deliveryDateDeadline'].widget = DatePickerField(format="%d.%m.%Y",)
        self.fields['deliveryDateDeadline'].input_formats = ["%d.%m.%Y"]

        self.fields['customer'].widget = SelectWithPop(Customer)
        self.fields['customer'].queryset = Customer.objects.filter_current_company()
        self.fields['responsible'].queryset = User.objects.filter_current_company()

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_pid(self):
        pid = self.cleaned_data['pid']

        projects = Project.objects.filter_current_company()
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
        self.fields['customer'].queryset = Customer.objects.filter_current_company()
        self.fields['responsible'].queryset = User.objects.filter_current_company()

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_pid(self):
        pid = self.cleaned_data['pid']

        projects = Project.objects.filter_current_company()
        for i in projects:
            if self.id == i.id:
                continue

            if i.pid == pid:
                raise forms.ValidationError("Det kreves unikt prosjektnr")

        return pid


class MilestoneForm(ModelForm):
    class Meta:
        model = Milestone
        fields = ("name", "description")