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
    admin_group = models.ForeignKey("group.Group", verbose_name="Ledergruppe", related_name="companiesWhereAdmin", null=True,
                                   blank=True)
    all_employees_group = models.ForeignKey("group.Group", verbose_name="Ansattegruppe",
                                          related_name="companiesWhereAllEmployeed", null=True, blank=True)
    days_into_next_month_hourregistration = models.IntegerField("Leveringsfrist", default=3)
    hours_needed_for_50_overtime_pay = models.IntegerField("Timer før 50%", default=160)
    hours_needed_for_100_overtime_pay = models.IntegerField("Timer før 100%", default=240)

    email_address   = models.CharField(max_length=100, null=True, blank=True)
    email_host      = models.CharField(max_length=100, null=True, blank=True)
    email_username  = models.CharField(max_length=100, null=True, blank=True)
    email_password  = models.CharField(max_length=100, null=True, blank=True)
            
    def __unicode__(self):
        return self.name

    def set_days_into_next_month(self, days):
        self.days_into_next_month_hourregistration = days
        self.save()

    def get_days_into_next_month(self):
        return self.days_into_next_month_hourregistration