# -*- coding: utf-8 -*-
from datetime import datetime, date
from decimal import Decimal
from app.customers.models import Customer
from helpers import calculateHoursWorked
from core import Core
from core.models import PersistentModel, User
from django.db import models
from django.core import urlresolvers
import time
import re

max_digits = 5
decimal_places = 3

class HourRegistration(PersistentModel):
    date = models.DateTimeField()
    order = models.ForeignKey('orders.Order')
    time_start = models.CharField(max_length=max_digits, null=True, default="")
    time_end = models.CharField(max_length=max_digits, null=True, default="")
    description = models.TextField(null=True, )

    pause = models.DecimalField(decimal_places=decimal_places, max_digits=max_digits, default=Decimal("0.0"),
                                blank=True)
    hourly_rate = models.DecimalField(null=True, blank=True, decimal_places=decimal_places, max_digits=max_digits)
    percent_cover = models.DecimalField(null=True, blank=True, decimal_places=decimal_places, max_digits=max_digits)
    hours_worked = models.DecimalField(blank=True, decimal_places=decimal_places, max_digits=max_digits)

    savedHours = models.DecimalField(decimal_places=decimal_places, max_digits=max_digits, null=True, blank=True,
                                     default=Decimal("0.0"))

    usedOfSavedHours = models.DecimalField(decimal_places=decimal_places, max_digits=max_digits, null=True, blank=True,
                                           default=Decimal("0.0"))

    def __unicode__(self):
        return unicode(self.date)

    def get_edit_url(self):
        return urlresolvers.reverse('app.hourregistrations.views.edit', args=("%s" % self.id,))

    def format_date(self):
        if re.match("\d\d:\d$", self.time_start):
            self.time_start = self.time_start + "0"
        elif re.match("\d:\d\d", self.time_start):
            self.time_start = "0" + self.time_start
        if re.match("\d\d:\d$", self.time_end):
            self.time_end = self.time_end + "0"
        elif re.match("\d:\d\d", self.time_end):
            self.time_end = "0" + self.time_end

    def save(self, *args, **kwargs):
        """
       Checks length of H:i, if in need of extend to a complete clock
        """
        self.format_date()

        new = False
        if not self.id:
            new = True

        if self.time_start and self.time_end:
            start = time.strptime("%s %s" % (self.date.strftime("%d.%m.%Y"), self.time_start), "%d.%m.%Y  %H:%M")
            end = time.strptime("%s %s" % (self.date.strftime("%d.%m.%Y"), self.time_end), "%d.%m.%Y  %H:%M")

            start_t = time.mktime(start)
            end_t = time.mktime(end)

            self.hours_worked = Decimal(calculateHoursWorked(start_t, end_t)) - Decimal(self.pause)
            #self.hours_worked = calculateHoursWorked(start_t, end_t)-self.pause-(self.savedHours - self.usedOfSavedHours)

        super(HourRegistration, self).save()

        #Have to wait to set this, because creator is not set before first save
        if self.creator:
            self.hourly_rate = self.creator.hourly_rate
            self.percent_cover = self.creator.percent_cover
            #Save again
        super(HourRegistration, self).save()


class HourRegisrationImage(PersistentModel):
    pass


class Disbursement(PersistentModel):
    HourRegistration = models.ForeignKey(HourRegistration, related_name="disbursements")
    description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="uploads/disbursements/")

    def __unicode__(self):
        return "Disbusment for %s" % self.HourRegistration

class DrivingRegistration(PersistentModel):
    HourRegistration = models.ForeignKey(HourRegistration, related_name="drivingregistration")
    time_start = models.CharField(max_length=5)
    time_end = models.CharField(max_length=5)
    kilometres = models.IntegerField()
    description = models.CharField(max_length=100)

def __unicode__(self):
    return "DrivingRegistration for %s" % self.HourRegistration

def initial_data ():
    pass