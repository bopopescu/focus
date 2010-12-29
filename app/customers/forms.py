# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *
from app.contacts.models import Contact
from core.widgets import *

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset = Contact.objects.for_company()

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_cid(self):
        cid = self.cleaned_data['cid']

        customers = Customer.objects.for_company()

        for i in customers:
            if self.id == i.id:
                continue

            if i.cid == cid:
                raise forms.ValidationError("Det kreves unikt kundenr")

        return cid


class CustomerFormSimple(ModelForm):
    class Meta:
        model = Customer
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'projects',)

    def __init__(self, *args, **kwrds):
        super(CustomerFormSimple, self).__init__(*args, **kwrds)
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset = Contact.objects.for_company()