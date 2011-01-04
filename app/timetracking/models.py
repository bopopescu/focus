from datetime import datetime
import re
from app.customers.models import Customer
from app.orders.models import Order
from core import Core
from core.models import PersistentModel, User
from django.db import models

class TypeOfTimeTracking(PersistentModel):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        new = False
        if not self.id:
            new = True

        super(TypeOfTimeTracking, self).save()

        #Give the user who created this ALL permissions on object

        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()
            allemployeesgroup = Core.current_user().get_company_allemployeesgroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

            if allemployeesgroup:
                allemployeesgroup.grant_role("Member", self)

class Timetracking(PersistentModel):
    date = models.DateTimeField()
    order = models.ForeignKey(Order)
    typeOfWork = models.ForeignKey(TypeOfTimeTracking)
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

        super(Timetracking, self).save()

        if self.creator:
            self.hourly_rate = self.creator.hourly_rate
            self.percent_cover = self.creator.percent_cover

        super(Timetracking, self).save()

        #Give the user who created this ALL permissions on object
        if new:
            Core.current_user().grant_role("Owner", self)
            adminGroup = Core.current_user().get_company_admingroup()

            if adminGroup:
                adminGroup.grant_role("Admin", self)

def initial_data ():
    #Create default time tracking types
    TypeOfTimeTracking.objects.get_or_create(name="Kontorarbeid")
    TypeOfTimeTracking.objects.get_or_create(name="Montering")

    a, created = User.objects.all().get_or_create(username="superadmin",
                                                  first_name="SuperAdmin",
                                                  last_name="",
                                                  canLogin=True,
                                                  is_superuser=True,
                                                  is_staff=True,
                                                  hourly_rate = 120,
                                                  percent_cover = 20,
                                                  is_active=True)

    testCustomer, created = Customer.objects.get_or_create(cid="100", full_name="Per", email="test@test.com")
    testOrder, created = Order.objects.get_or_create(oid="100", order_name="TestOrdre", customer=testCustomer)

    t = Timetracking.objects.create(date=datetime.strptime("10.10.2010", "%d.%m.%Y"),
                                    order=testOrder,
                                    time_start="20:10",
                                    time_end="22:10",
                                    description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("2.10.2010", "%d.%m.%Y"),
                                    order=testOrder,
                                    time_start="20:10",
                                    time_end="22:10",
                                    description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("15.10.2010", "%d.%m.%Y"),
                                    order=testOrder,
                                    time_start="20:10",
                                    time_end="22:10",
                                    description="Dette er en test")

    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("10.5.2010", "%d.%m.%Y"),
                                order=testOrder,
                                time_start="20:10",
                                time_end="22:10",
                                description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("15.5.2010", "%d.%m.%Y"),
                                order=testOrder,
                                time_start="20:10",
                                time_end="22:10",
                                description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("1.5.2010", "%d.%m.%Y"),
                                order=testOrder,
                                time_start="20:10",
                                time_end="22:10",
                                description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("10.08.2009", "%d.%m.%Y"),
                                order=testOrder,
                                time_start="20:10",
                                time_end="22:10",
                                description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("4.08.2009", "%d.%m.%Y"),
                                order=testOrder,
                                time_start="20:10",
                                time_end="22:10",
                                description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)

    t = Timetracking.objects.create(date=datetime.strptime("10.08.2009", "%d.%m.%Y"),
                                order=testOrder,
                                time_start="20:10",
                                time_end="22:10",
                                description="Dette er en test")
    t.creator = a
    t.save()
    a.grant_role("Owner", t)