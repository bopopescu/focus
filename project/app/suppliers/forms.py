# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.suppliers.models import Supplier

class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ("name", "email", "phone", "zip", "address")

    def __init__(self, *args, **kwrds):
        super(SupplierForm, self).__init__(*args, **kwrds)
        #self.fields['contacts'].widget = MultipleSelectWithPop(Contact)
        #self.fields['contacts'].queryset = Contact.objects.all()


class SupplierSimpleForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ("name", "email", "phone", "address")