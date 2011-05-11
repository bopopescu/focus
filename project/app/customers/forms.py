# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.contacts.forms import ContactField
from models import Customer
from django.utils.translation import ugettext as _
from django.forms import forms


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        #exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')
        fields = ("cid", "name", "email", "address", "phone", "zip", "website",'invoice_zip','invoice_address')

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
        fields = ("cid", "name", "email", "phone", "website","address", "zip", 'invoice_zip','invoice_address' )
        #exclude = ('deleted', 'trashed','date_created', 'date_edited', 'owner', 'creator', 'editor', 'company', 'projects', )

    def __init__(self, *args, **kwrds):
        super(CustomerFormSimple, self).__init__(*args, **kwrds)
        #self.fields['contacts'].queryset = Contact.objects.all()


class ContactToCustomerForm(forms.Form):
    contact = ContactField()