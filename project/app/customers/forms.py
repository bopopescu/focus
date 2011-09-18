# -*- coding: utf-8 -*-
from app.contacts.models import Contact
from core import Core
from django.forms import ModelForm
from models import Customer
from django.utils.translation import ugettext as _
from django import forms

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        #exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')
        fields = ("cid", "name", "email", "phone", "website", "address", "zip", 'invoice_address', 'invoice_zip',)

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)

        if 'instance' in kwargs:
            self.id = kwargs['instance'].id

    def clean_cid(self):
        cid = self.cleaned_data['cid']

        customers = Customer.objects.filter_current_company()

        for i in customers:
            if self.id == i.id:
                continue
            if i.cid == cid:
                raise forms.ValidationError(_("You need to use a unique customer number"))
        return cid


class CustomerFormSimple(ModelForm):
    class Meta:
        model = Customer
        fields = ("cid", "name", "email", "phone", "website", "address", "zip", 'invoice_address', 'invoice_zip', )
        #exclude = ('deleted', 'trashed','date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'projects', )

    def __init__(self, *args, **kwrds):
        super(CustomerFormSimple, self).__init__(*args, **kwrds)
        #self.fields['contacts'].queryset = Contact.objects.all()


class ContactToCustomerForm(forms.Form):
    contact = forms.ModelChoiceField(queryset=Contact.objects.all())

    def __init__(self, *args, **kwargs):
        super(ContactToCustomerForm, self).__init__(args, kwargs)
        contacts = Core.current_user().get_permitted_objects("VIEW", Contact).filter(trashed=False)
        self.fields['contact'].queryset = contacts