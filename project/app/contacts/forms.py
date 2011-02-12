# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.contacts.models import *

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('deleted', 'trashed','date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')