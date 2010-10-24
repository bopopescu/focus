from django.db import models
from core.models import PersistentModel

class Valuta(PersistentModel):
    name = models.CharField(max_length=50)
    currentValue = models.CharField(max_length=150)

    def __unicode__(self):
        return self.name

class UnitsForSizes(PersistentModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class ProductGroup(PersistentModel):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Product(PersistentModel):
    name = models.CharField(max_length=100)
    countOfAvailableInStock = models.CharField(max_length=10)

    group = models.ForeignKey(ProductGroup, related_name="products")

    size = models.CharField(max_length=100)
    unitForSize = models.ForeignKey(UnitsForSizes)

    price = models.CharField(max_length=100)
    priceVal = models.ForeignKey(Valuta, related_name="products")

    def __unicode__(self):
        return self.name

