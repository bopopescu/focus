# -*- coding: utf-8 -*-
from datetime import datetime, date
from decimal import Decimal
import os
from django.conf import settings
from app.customers.models import Customer
from django.core.files.storage import FileSystemStorage
from helpers import calculateHoursWorked
from core import Core
from core.models import PersistentModel, User
from django.db import models
from django.core import urlresolvers
import time
import re
from django.utils.translation import ugettext as _

max_digits = 5
decimal_places = 2

fs = FileSystemStorage(location=os.path.join(settings.BASE_PATH, "uploads"))

class HourRegistrationType(PersistentModel):
    name = models.CharField(max_length=100)
    rate = models.DecimalField(decimal_places=decimal_places, max_digits=max_digits, null=True)

    def __unicode__(self):
        return self.name

    def get_edit_url(self):
        return urlresolvers.reverse('app.hourregistrations.views.admin_hourregistrationtypes', args=("%s" % self.id,))


class HourRegistration(PersistentModel):
    date = models.DateTimeField(verbose_name=_("Date"))

    order = models.ForeignKey('orders.Order', related_name="hourregistrations", verbose_name=_("Order"), null=True)
    ticket = models.ForeignKey("tickets.Ticket", related_name="hourregistrations", null=True, blank=True, verbose_name=_("Ticket"))

    type = models.ForeignKey(HourRegistrationType, related_name="hourregistrations",verbose_name=_("Type"))

    time_start = models.CharField(max_length=max_digits, null=True, blank=True, default="", verbose_name=_("Time start"))
    time_end = models.CharField(max_length=max_digits, null=True, blank=True, default="", verbose_name=_("Time end"))

    description = models.TextField(null=True, verbose_name=_("Description"))

    hours = models.DecimalField(null=True, decimal_places=decimal_places, max_digits=max_digits, verbose_name=_("Hours"))
    hourly_rate = models.DecimalField(null=True, blank=True, decimal_places=decimal_places, max_digits=max_digits, verbose_name=_("Hourly rate"))

    def __unicode__(self):
        return unicode(self.date)

    def get_order_name(self):
        if self.order:
            return self.order.title
        return ""

    def get_customer_name(self):
        if self.order:
            if self.order.customer:
                return self.order.customer.name
        return ""

    def save(self, *args, **kwargs):
        super(HourRegistration, self).save(noNotification=True)

        #Have to wait to set this, because creator is not set before first save
        if self.creator:
            self.hourly_rate = self.creator.hourly_rate

        super(HourRegistration, self).save(noNotification=True)

    def get_edit_url(self):
        return urlresolvers.reverse('app.hourregistrations.views.edit', args=("%s" % self.id,))


class Disbursement(PersistentModel):
    date = models.DateField()
    order = models.ForeignKey('orders.Order', related_name="disbursements", null=True)
    description = models.CharField(max_length=100, default="", null=True)
    rate = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    count = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    attachment = models.ImageField(upload_to="disbursements", storage=fs, blank=True, null=True)

    def __unicode__(self):
        return "Disbusment %s" % self.date

    def get_sum(self):
        return self.rate*self.count

    def get_edit_url(self):
        return urlresolvers.reverse('app.hourregistrations.views.disbursements', args=("%s" % self.id,))