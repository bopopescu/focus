# -*- coding: utf-8 -*-

from django.forms import ModelForm
from models import *
from core.widgets import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'productGroup', 'countOfAvailableInStock', 'size', 'price', 'unitForSize', 'priceVal',
                  'normalDeliveryTime')

    def __init__(self, *args, **kwrds):
        super(ProductForm, self).__init__(*args, **kwrds)
        self.fields['unitForSize'].widget = SelectWithPop()
        self.fields['unitForSize'].queryset = UnitsForSizes.objects.all()
        self.fields['priceVal'].widget = SelectWithPop()
        self.fields['priceVal'].queryset = Currency.objects.all()
        self.fields['productGroup'].widget = SelectWithPop()
        self.fields['productGroup'].queryset = ProductGroup.objects.all()

class ProductGroupForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name',)

class CurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = ('name', 'sign', 'value')

class UnitsForSizesForm(ModelForm):
    class Meta:
        model = UnitsForSizes
        fields = ('name',)

class ProductFileForm(ModelForm):
    class Meta:
           model = ProductFile
           fields = ('name','file')