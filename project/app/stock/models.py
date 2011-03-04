# -*- coding: utf-8 -*-

from django.db import models
from core.models import PersistentModel
from app.suppliers.models import Supplier
from django.core import urlresolvers

class UnitsForSizes(PersistentModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.stock.views.productunit.add_ajax')

    @staticmethod
    def simpleform():
        return UnitsForSizesForm(instance=UnitsForSizes(), prefix="units")

class ProductCategory(PersistentModel):
    name = models.CharField("Navn", max_length=100)

    def __unicode__(self):
        return self.name

class ProductGroup(PersistentModel):
    name = models.CharField("Navn", max_length=100)
    category = models.ForeignKey(ProductCategory, verbose_name="Kategori", related_name="productgroups", null=True)

    def __unicode__(self):
        return self.name

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.stock.views.productgroup.add_ajax')

    @staticmethod
    def simpleform():
        return ProductGroupForm(instance=ProductGroup(), prefix="productgroups")

    def getViewUrl(self):
        return urlresolvers.reverse('app.stock.views.productgroup.edit', args=("%s" % self.id,))

class Currency(PersistentModel):
    name = models.CharField("Navn", max_length=100)
    sign = models.CharField("Tegn ($, kr) osv", max_length=10)
    value = models.CharField("Verdi", max_length=100)

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.stock.views.currency.add_ajax')

    @staticmethod
    def simpleform():
        return CurrencyForm(instance=Currency(), prefix="currencies")

    def __unicode__(self):
        return self.name

class Product(PersistentModel):
    pid = models.IntegerField("Varenr", null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.CharField("Pris", max_length=100, null=True)
    price_out = models.CharField("Pris ut", max_length=100, null=True)
    max_discount = models.CharField("Maks prosentavslag", max_length=5, null=True)
    countOfAvailableInStock = models.CharField("Lagerstatus", max_length=10)
    supplier = models.ForeignKey(Supplier, related_name="products", null=True)
    size = models.CharField(max_length=100)
    unitForSize = models.ForeignKey(UnitsForSizes, verbose_name="Enhet")
    priceVal = models.ForeignKey(Currency, related_name="products", verbose_name="Valuta")
    normalDeliveryTime = models.CharField("Normal leveringstid", max_length=10, null=True)
    productGroup = models.ForeignKey(ProductGroup, related_name="products", null=True)

    def __unicode__(self):
        return self.name

    def getViewUrl(self):
        return urlresolvers.reverse('app.stock.views.product.view', args=("%s" % self.id,))

    def getEditUrl(self):
        return urlresolvers.reverse('app.stock.views.product.edit', args=("%s" % self.id,))

    def getDeleteUrl(self):
        return urlresolvers.reverse('app.stock.views.product.delete', args=("%s" % self.id,))

    def getRecoverUrl(self):
        return urlresolvers.reverse('app.stock.views.product.recover', args=("%s" % self.id,))

class ProductFile(PersistentModel):
    product = models.ForeignKey(Product, related_name="files")
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="uploads/products")

    def getFile(self):
        return "/media/%s" % self.file


from app.stock.forms import ProductGroupForm, UnitsForSizesForm, CurrencyForm