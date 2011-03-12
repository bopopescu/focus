# -*- coding: utf-8 -*-

from django.forms import ModelForm
from models import *
from core.widgets import *
from functools import partial
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'productGroup', 'countOfAvailableInStock', 'normalDeliveryTime', 'unitForSize', 'size',
                  'price', 'priceVal', 'supplier',)

    def __init__(self, *args, **kwrds):
        super(ProductForm, self).__init__(*args, **kwrds)

        self.fields['unitForSize'].widget = SelectWithPop(UnitsForSizes)
        self.fields['unitForSize'].queryset = UnitsForSizes.objects.inCompany()

        self.fields['priceVal'].widget = SelectWithPop(Currency)
        self.fields['priceVal'].queryset = Currency.objects.all()

        self.fields['productGroup'].widget = SelectWithPop(ProductGroup)
        self.fields['productGroup'].queryset = ProductGroup.objects.inCompany()

        self.fields['supplier'].widget = SelectWithPop(Supplier)
        self.fields['supplier'].queryset = Supplier.objects.inCompany()

class ProductGroupForm(ModelForm):
    class Meta:
        model = Product
        fields = ('name',)

class CurrencyForm(ModelForm):
    class Meta:
        model = Currency
        fields = ('name', 'sign', 'value',)

class UnitsForSizesForm(ModelForm):
    class Meta:
        model = UnitsForSizes
        fields = ('name',)

class ProductFileForm(ModelForm):
    class Meta:
        model = ProductFile
        fields = ('name', 'file',)


class ProductAutocompleteWidget(JQueryAutoComplete):
    def __init__(self):
        JQueryAutoComplete.__init__(self, source=partial(reverse, 'app.stock.views.product.autocomplete'))

class ProductField(forms.Field):
    widget = ProductAutocompleteWidget() # Default widget to use when rendering this type of Field.
    def __init__(self,  *args, **kwargs):
        #self.max_length, self.min_length = max_length, min_length
        super(ProductField, self).__init__(*args, **kwargs)

    def clean(self, value):
        """Checks that the user exists, and returns a user object"""
        super(ProductField, self).clean(value)
        try:
            product = Product.objects.get(name=value)
        except:
            raise forms.ValidationError(_("Product with name %(name)s does not exist")  % {'name':value})
        return product