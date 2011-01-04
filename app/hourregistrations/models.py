from datetime import datetime, date
import time
import re
from app.customers.models import Customer
from app.hourregistrations.helpers import calculateHoursWorked
from app.orders.models import Order
from core import Core
from core.models import PersistentModel, User
from django.db import models

class TypeOfHourRegistration(PersistentModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(TypeOfHourRegistration, self).save()

        #Give the user who created this ALL permissions on object

        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)

class HourRegistration(PersistentModel):
    date = models.DateTimeField()
    order = models.ForeignKey(Order)
    typeOfWork = models.ForeignKey(TypeOfHourRegistration)
    time_start = models.CharField(max_length=5)
    time_end = models.CharField(max_length=5)
    description = models.TextField()

    hourly_rate = models.IntegerField(null=True)
    percent_cover = models.IntegerField(null=True)
    hours_worked = models.DecimalField(decimal_places=3, max_digits=5)

    def __unicode__(self):
        return unicode(self.date)

    def save(self, *args, **kwargs):
        """
       Checks length of H:i, if in need of extend to a complete clock
        """

        if re.match("\d\d:\d$", self.time_start):
            self.time_start = self.time_start + "0"

        if re.match("\d:\d\d", self.time_start):
            self.time_start = "0" + self.time_start

        if re.match("\d\d:\d$", self.time_end):
            self.time_end = self.time_end + "0"

        if re.match("\d:\d\d", self.time_end):
            self.time_end = "0" + self.time_end

        new = False
        if not self.id:
            new = True

        if self.time_start and self.time_end:
            start = time.strptime("%s %s" % (self.date.strftime("%d.%m.%Y"), self.time_start), "%d.%m.%Y  %H:%M")
            end = time.strptime("%s %s" % (self.date.strftime("%d.%m.%Y"), self.time_end), "%d.%m.%Y  %H:%M")

            start_t = time.mktime(start)
            end_t = time.mktime(end)

            self.hours_worked = calculateHoursWorked(start_t, end_t)

        super(HourRegistration, self).save()

        #Have to wait to set this, because creator is not set before first save
        if self.creator:
            self.hourly_rate = self.creator.hourly_rate
            self.percent_cover = self.creator.percent_cover
            #Save again
        super(HourRegistration, self).save()

        #Give the user who created this ALL permissions on object
        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)


class HourRegisrationImage(PersistentModel):
    pass

class Disbursement(PersistentModel):
    HourRegistration = models.ForeignKey(HourRegistration, related_name="disbursements")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="uploads/disbursements/")

    def __unicode__(self):
        return "Disbusment for %s" % self.HourRegistration

def initial_data ():
    #Create default time tracking types
    type = TypeOfHourRegistration.objects.get_or_create(name="Kontorarbeid")[0]

    a, created = User.objects.all().get_or_create(username="superadmin",
                                                  first_name="SuperAdmin",
                                                  last_name="",
                                                  canLogin=True,
                                                  is_superuser=True,
                                                  is_staff=True,
                                                  hourly_rate=120,
                                                  percent_cover=20,
                                                  is_active=True)
    Core.set_test_user(a)

    testCustomer, created = Customer.objects.get_or_create(cid="100", full_name="Per", email="test@test.com")
    testOrder, created = Order.objects.get_or_create(oid="100", order_name="TestOrdre", customer=testCustomer)

    t = HourRegistration.objects.create(date=datetime.strptime("10.10.2010", "%d.%m.%Y"),
                                        order=testOrder,
                                        time_start="20:10",
                                        typeOfWork=type,
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("2.10.2010", "%d.%m.%Y"),
                                        order=testOrder,
                                        typeOfWork=type,
                                        time_start="20:10",
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("15.10.2010", "%d.%m.%Y"),
                                        order=testOrder,
                                        typeOfWork=type,
                                        time_start="20:10",
                                        time_end="22:10",
                                        description="Dette er en test")

    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("10.5.2010", "%d.%m.%Y"),
                                        order=testOrder,
                                        typeOfWork=type,
                                        time_start="20:10",
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("15.5.2010", "%d.%m.%Y"),
                                        order=testOrder,
                                        time_start="20:10",
                                        typeOfWork=type,
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("1.5.2010", "%d.%m.%Y"),
                                        order=testOrder,
                                        typeOfWork=type,
                                        time_start="20:10",
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("10.08.2009", "%d.%m.%Y"),
                                        order=testOrder,
                                        typeOfWork=type,
                                        time_start="20:10",
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("4.08.2009", "%d.%m.%Y"),
                                        order=testOrder,
                                        time_start="20:10",
                                        typeOfWork=type,
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = HourRegistration.objects.create(date=datetime.strptime("10.08.2009", "%d.%m.%Y"),
                                        order=testOrder,
                                        time_start="20:10",
                                        typeOfWork=type,
                                        time_end="22:10",
                                        description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)