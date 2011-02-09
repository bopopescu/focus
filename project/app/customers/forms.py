# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Customer
from app.contacts.models import Contact
from core.widgets import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        #exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')
        fields = ("cid", "full_name","email","address","phone","zip","city","website","alternative_address","contacts")

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset = Contact.objects.all()

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_cid(self):
        cid = self.cleaned_data['cid']

        customers = Customer.objects.inCompany()

        for i in customers:
            if self.id == i.id:
                continue

            if i.cid == cid:
                raise forms.ValidationError("Det kreves unikt kundenr")

        return cid

class CustomerFormSimple(ModelForm):
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'projects','contacts')

    def __init__(self, *args, **kwrds):
        super(CustomerFormSimple, self).__init__(*args, **kwrds)
        #self.fields['contacts'].queryset = Contact.objects.all()