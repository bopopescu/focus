# -*- coding: utf-8 -*-
from django.forms import ModelForm

from models import *
from app.contacts.models import Contact

from core.widgets import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')

    def __init__(self, *args, **kwrds):
        super(CustomerForm, self).__init__(*args, **kwrds)
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset = Contact.objects.for_company()

class CustomerFormSimple(ModelForm):
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'projects',)

    def __init__(self, *args, **kwrds):
        super(CustomerFormSimple, self).__init__(*args, **kwrds)
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset = Contact.objects.for_company()