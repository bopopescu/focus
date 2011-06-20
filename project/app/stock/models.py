# -*- coding: utf-8 -*-

from django.db import models
from app.files.models import File
from core.models import PersistentModel
from app.suppliers.models import Supplier
from django.core import urlresolvers
from django.utils.translation import ugettext as _

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

    def get_view_url(self):
        return urlresolvers.reverse('app.stock.views.productgroup.edit', args=("%s" % self.id,))


class Currency(PersistentModel):
    name = models.CharField("Navn", max_length=100)
    iso = models.CharField("Verdi", max_length=100, null=True)
    value = models.DecimalField(decimal_places=2, max_digits=5, default=0)

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.stock.views.currency.add_ajax')

    @staticmethod
    def simpleform():
        return CurrencyForm(instance=Currency(), prefix="currencies")

    def __unicode__(self):
        return self.name

class Product(PersistentModel):
    pid = models.CharField(_("ProductID"), max_length=50, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.CharField(_("Price in"), max_length=100, null=True)
    price_out = models.CharField(_("Price out"), max_length=100, null=True)
    max_discount = models.CharField(_("Max discount"), max_length=5, null=True)
    countOfAvailableInStock = models.CharField(_("Avaiable in stock"), max_length=10)
    supplier = models.ForeignKey(Supplier, related_name="products", null=True)
    size = models.CharField(max_length=100, null=True)
    unitForSize = models.ForeignKey(UnitsForSizes, verbose_name=_("Unit"), null=True)
    priceVal = models.ForeignKey(Currency, related_name="products", verbose_name=_("Currency"))
    normalDeliveryTime = models.CharField(_("Expected delivery time"), max_length=10, null=True)
    productGroup = models.ForeignKey(ProductGroup, related_name="products", null=True)
    files = models.ManyToManyField(File)
        
    def __unicode__(self):
        return self.name

    @staticmethod
    def calculate_next_pid():
        return Product.objects.filter_current_company().count()+1

    def can_be_deleted(self):
        can_be_deleted = True
        reasons = []

        if self.orders().all().count() > 0:
            can_be_deleted = False
            reasons.append(_("Product used in orders, see orders menu in sidebar."))

        if can_be_deleted:
            return (True, "OK")

        return (False, reasons)

    def get_view_url(self):
        return urlresolvers.reverse('app.stock.views.product.view', args=("%s" % self.id,))

    def get_edit_url(self):
        return urlresolvers.reverse('app.stock.views.product.edit', args=("%s" % self.id,))

    def get_delete_url(self):
        return urlresolvers.reverse('app.stock.views.product.delete', args=("%s" % self.id,))

    def get_recover_url(self):
        return urlresolvers.reverse('app.stock.views.product.recover', args=("%s" % self.id,))

    def orders(self):
        orderIDs = []
        cls = None
        for line in self.order_lines.all():
            if not cls:
                cls = line.order.__class__
            if not line.order.id in orderIDs:
                orderIDs.append(line.order.id)
        orders = cls.objects.filter(id__in=orderIDs)
        return orders

def initial_data ():
    Currency.objects.get_or_create(name="Norsk Krone", iso="NOK")
    Currency.objects.get_or_create(name="Dansk Krone", iso="DKK")
    Currency.objects.get_or_create(name="Svensk krona", iso="SEK")
    Currency.objects.get_or_create(name="Pound sterling", iso="GBP")
    Currency.objects.get_or_create(name="US Dollar", iso="USD")
    Currency.objects.get_or_create(name="Euro", iso="EUR")

from app.stock.forms import UnitsForSizesForm, ProductGroupForm, CurrencyForm
