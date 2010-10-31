from django.db import models
from core.models import PersistentModel
from app.suppliers.models import Supplier

class UnitsForSizes(PersistentModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class ProductCategory(PersistentModel):
    name = models.CharField("Navn", max_length=100)

    def __unicode__(self):
        return self.name

class ProductGroup(PersistentModel):
    name = models.CharField("Navn", max_length=100)
    category = models.ForeignKey(ProductCategory, verbose_name = "Kategori", related_name="productgroups", null=True)

    def __unicode__(self):
        return self.name

class Currency(PersistentModel):
    name = models.CharField("Navn", max_length=100)
    sign = models.CharField("Tegn ($, kr) osv", max_length=10)
    value= models.CharField("Verdi", max_length=100)

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
