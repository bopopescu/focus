# -*- coding: utf-8 -*-
from django.forms import ModelForm
from functools import partial
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from app.stock.models import Product, UnitsForSizes, ProductGroup, Currency
from app.suppliers.models import Supplier
from core.widgets import SelectWithPop
from django.forms import forms

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('pid', 'name', 'productGroup', 'countOfAvailableInStock', 'normalDeliveryTime', 'unitForSize', 'size',
                  'price', 'price_out', 'max_discount', 'priceVal', 'supplier','description')

    def __init__(self, *args, **kwrds):
        super(ProductForm, self).__init__(*args, **kwrds)

        self.fields['unitForSize'].widget = SelectWithPop(UnitsForSizes)
        self.fields['unitForSize'].queryset = UnitsForSizes.objects.filter_current_company()

        self.fields['productGroup'].widget = SelectWithPop(ProductGroup)
        self.fields['productGroup'].queryset = ProductGroup.objects.filter_current_company()

        self.fields['supplier'].widget = SelectWithPop(Supplier)
        self.fields['supplier'].queryset = Supplier.objects.filter_current_company()


class ProductGroupForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name',)


class CurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = ('name', 'value', 'iso',)


class UnitsForSizesForm(ModelForm):
    class Meta:
        model = UnitsForSizes
        fields = ('name',)