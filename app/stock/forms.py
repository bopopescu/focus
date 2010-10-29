 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields= ('name','group','countOfAvailableInStock','size','price','unitForSize','priceVal',)


class ProductGroupForm(ModelForm):
    class Meta:
        model = Product
        fields= ('name',)