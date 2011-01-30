# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *

class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = ('deleted', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')