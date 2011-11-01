from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from app.calendar.forms import EventForm, RepeatOptionForm, EventTypeForm
from app.calendar.models import Event, RepeatOption, EventType
from core import Core
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY
import calendar
from django.utils.translation import ugettext as _

from core.auth.user.models import User
from core.decorators import require_permission


def get_month_link(param, year, month):
    if param == "next":
        if month==12:
            month=1
            year +=1
        else:
            month+=1

    else:
        if month==1:
            month = 12
            year -=1
        else:
            month-=1
            
    return "/calendar/%s/%s/" % (year,month)

def overview(request, year=datetime.now().year, month=datetime.now().month):
    year = int(year)
    month = int(month)

    days_in_month = calendar.monthrange(year, month)

    cal = {}

    users = User.objects.filter_current_company()

    for user in users:
        cal[user] = {}

        for day in range(1, days_in_month[1] + 1):
            cal[user][day] = []

        for event in user.events.all():
            for date in event.get_dates():
                if date.year == year and date.month == month:
                    cal[user][date.day].append(event)

    return render(request, "calendar/calendar.html", {'cal': cal,
                                                      'days_in_month': range(1, days_in_month[1] + 1),
                                                      'current_month': (year,month),
                                                      'next_month_link':get_month_link("next", year, month),
                                                      'last_month_link':get_month_link("last", year, month)
                                                    })


def add(request):
    return form(request)


def edit(request, id):
    return form(request, id)


def form (request, id=False):
    if id:
        instance = get_object_or_404(Event, id=id, deleted=False)
        msg = _("Successfully edited contact")
    else:
        instance = Event()
        msg = _("Successfully added new contact")

        
    repeat_instance = RepeatOption()
    if instance.repeat:
        repeat_instance = instance.repeat

    if request.method == 'POST':
        event_form = EventForm(request.POST, instance=instance)
        repeat_form = RepeatOptionForm(request.POST, instance=repeat_instance)

        if event_form.is_valid():
            event = event_form.save()

            if repeat_form.is_valid():
                event.repeat = repeat_form.save()
                event.save()

            return redirect(overview)

    else:
        event_form = EventForm(instance=instance)
        repeat_form = RepeatOptionForm(instance=repeat_instance)

    return render(request, "calendar/form.html", {'title': _("Event"),
                                                  'event': instance,
                                                  'event_form': event_form,
                                                  'repeat_form': repeat_form,
                                                  })


def event_type_add(request):
    return event_type_form(request)


def event_type_edit(request, id):
    return event_type_form(request, id)


def event_type_form (request, id=False):
    if id:
        instance = get_object_or_404(EventType, id=id, deleted=False)
        msg = _("Successfully edited contact")
    else:
        instance = EventType()
        msg = _("Successfully added new contact")

    if request.method == 'POST':
        form = EventTypeForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()

            return redirect(overview)

    else:
        form = EventTypeForm(instance=instance)

    return render(request, "form.html", {'title': _("Event types"),
                                                  'form': form,
                                                  })
