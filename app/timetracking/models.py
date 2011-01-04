import re
from app.orders.models import Order
from core import Core
from core.models import PersistentModel
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
    date = models.DateField()
    order = models.ForeignKey(Order)
    typeOfWork = models.ForeignKey(TypeOfTimeTracking)
    time_start = models.CharField(max_length=5)
    time_end = models.CharField(max_length=5)
    description = models.TextField()

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