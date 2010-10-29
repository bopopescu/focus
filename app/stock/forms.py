 # -*- coding: utf-8 -*-
from django.forms import ModelForm
from django import forms

from models import *

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields= ('name','countOfAvailableInStock','group','size','unitForSize','price','priceVal',)