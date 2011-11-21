# -*- coding: utf-8 -*-
from django.forms import forms
from django.forms import ModelForm
from app.contacts.models import Contact
from functools import partial
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

class ContactImageForm(ModelForm):
    class Meta:
        model = Contact
        fields = ("image",)


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = (
        'deleted', 'image', 'trashed', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')