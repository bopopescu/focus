# -*- coding: utf-8 -*-
from django.forms import forms
from django.forms import ModelForm
from app.contacts.models import Contact
from core.widgets import JQueryAutoComplete
from functools import partial
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

class ContactWidget(JQueryAutoComplete):
    def __init__(self):
        JQueryAutoComplete.__init__(self, source=partial(reverse, 'app.contacts.views.list_ajax'))


class ContactImageForm(ModelForm):
    class Meta:
        model = Contact
        fields = ("image",)


class ContactForm(ModelForm):
    class Meta:
        model = Contact
        exclude = (
        'deleted', 'image', 'trashed', 'date_created', 'date_edited', 'owner', 'creator', 'editor', 'company')


class ContactAutocompleteWidget(JQueryAutoComplete):
    def __init__(self):
        JQueryAutoComplete.__init__(self, source=partial(reverse, 'app.contacts.views.autocomplete'))


class ContactField(forms.Field):
    widget = ContactAutocompleteWidget() # Default widget to use when rendering this type of Field.

    def __init__(self, *args, **kwargs):
        #self.max_length, self.min_length = max_length, min_length
        super(ContactField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """Checks that the user exists, and returns a user object"""
        super(ContactField, self).clean(value)
        try:
            product = Contact.objects.get(full_name=value)
        except:
            raise forms.ValidationError(_("Contact with name %(name)s does not exist") % {'name': value})
        return product