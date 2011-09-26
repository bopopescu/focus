# -*- coding: utf-8 -*-
from app.contacts.models import Contact
from core import Core
from django.db.models.query_utils import Q
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


class ContactParticipantToCustomerForm(forms.Form):
    contact = forms.ModelChoiceField(queryset=Contact.objects.none())

    def __init__(self, *args, **kwargs):
        existing_contacts = Q()

        if 'existing_contacts' in kwargs:
            existing_contacts = kwargs.get('existing_contacts')
            del kwargs['existing_contacts']

        super(ContactParticipantToCustomerForm, self).__init__(*args, **kwargs)
        qs = Core.current_user().get_permitted_objects("VIEW", Contact).filter(
            trashed=False)


        if existing_contacts:
            qs = qs.exclude(id__in=[contact.id for contact in existing_contacts])

        self.fields['contact'].queryset = qs