# -*- coding: utf-8 -*-
from django.db import models

"""
The Company class.
All users belong to a company, therefore all objects belongs to a company, like projects, orders...
A user can only see objects within the same company.
 * An exception to this, if the user is a guest in another companys project.
"""

class Company(models.Model):
    name = models.CharField(max_length=80)
    adminGroup = models.ForeignKey("group.Group", verbose_name="Ledergruppe", related_name="companiesWhereAdmin", null=True,
                                   blank=True)
    allEmployeesGroup = models.ForeignKey("group.Group", verbose_name="Ansattegruppe",
                                          related_name="companiesWhereAllEmployeed", null=True, blank=True)
    daysIntoNextMonthHourRegistration = models.IntegerField("Leveringsfrist", default=3)
    hoursNeededFor50overtimePay = models.IntegerField("Timer før 50%", default=160)
    hoursNeededFor100overtimePay = models.IntegerField("Timer før 100%", default=240)

    def __unicode__(self):
        return self.name

    def set_days_into_next_month(self, days):
        self.daysIntoNextMonthHourRegistration = days
        self.save()

    def get_days_into_next_month(self):
        return self.daysIntoNextMonthHourRegistration