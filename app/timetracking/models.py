from app.orders.models import *
from datetime import datetime
import re


class TypeOfTimeTracking(PersistentModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
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
            self.time_start = "0"+self.time_start

        if re.match("\d\d:\d$", self.time_end):
            self.time_end = self.time_end + "0"

        if re.match("\d:\d\d", self.time_end):
            self.time_end = "0"+self.time_end


        super(Timetracking, self).save()