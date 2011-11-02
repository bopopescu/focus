from datetime import datetime
from django.utils.translation import ugettext as _
from django.db import models
from core.models import User, PersistentModel

from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY
from django.core import urlresolvers

types = (
    ("daily", _('Daily')),
    ("weekly", _('Weekly')),
    ("monthly", _('Monthly')),
    )

class RepeatOption(PersistentModel):
    available_option = models.CharField(max_length=10, choices=types, blank=True)
    times = models.IntegerField(blank=True, null=True, default=0)
    repeat_until = models.DateTimeField(null=True, blank=True)

    def get_dates_for(self, event):
        dates = set([])

        if self.available_option and self.times:

            option = {'daily': DAILY, 'monthly': MONTHLY, 'weekly': WEEKLY}
            for date in list(rrule(option[self.available_option],
                                   interval=self.times,
                                   dtstart=event.start,
                                   until=self.repeat_until)):
                dates.add(date)

                for date in list(rrule(DAILY, dtstart=date, until=date+(event.end-event.start))):
                    dates.add(date)

        return dates

    def __unicode__(self):
        return self.available_option

event_type_colors = (
    ("red", _('Red')),
    ("blue", _('Blue')),
    ("green", _('Green')),
    ("orange", _('Orange')),
    ("gray", _('Gray')),
    )

class EventType(PersistentModel):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50, choices = event_type_colors)

    def __unicode__(self):
        return self.name

    @staticmethod
    def add_ajax_url():
        return urlresolvers.reverse('app.calendar.views.add_event_type_ajax')

    @staticmethod
    def simpleform():
        return EventTypeForm(instance=EventType(), prefix="event_type")


class Event(PersistentModel):
    start = models.DateTimeField()
    end = models.DateTimeField()

    title = models.CharField(max_length=100, default="")
    description = models.TextField()
    type = models.ForeignKey(EventType, null=True)
    
    users = models.ManyToManyField(User, related_name="events")

    repeat = models.ForeignKey(RepeatOption, null=True, blank=True)
    special_cases = models.ManyToManyField('Event', related_name="parent_event", null=True, blank=True)

    def __unicode__(self):
        return self.title

    def get_dates(self):
        dates = set([])

        for date in list(rrule(DAILY, dtstart=self.start, until=self.end)):
            dates.add(date)

        if self.repeat:
            for date in self.repeat.get_dates_for(self):
                dates.add(date)

        #cleaning up dates from special-cases
        for special_case in self.special_cases.all():
            for date in list(rrule(DAILY, dtstart=special_case.start, until=special_case.start+(self.end-self.start))):
                dates.remove(date)

            for date in special_case.get_dates():
                dates.add(date)

        return dates

from app.calendar.forms import EventTypeForm
