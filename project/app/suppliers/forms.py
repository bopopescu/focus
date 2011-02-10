# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import *
from core.widgets import MultipleSelectWithPop

class SupplierForm(ModelForm):
    def __init__(self, *args, **kwrds):
        super(SupplierForm, self).__init__(*args, **kwrds)
        self.fields['contacts'].widget = MultipleSelectWithPop()
        self.fields['contacts'].queryset = Contact.objects.all()

    class Meta:
        model = Supplier
        fields = ("name","contacts")