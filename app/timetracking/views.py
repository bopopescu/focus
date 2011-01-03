# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from app.timetracking.helpers import calculateHoursWorked
from core.decorators import require_permission, login_required
from forms import *
from core.shortcuts import *
from django.contrib import messages
from django.utils.html import escape
from core.views import updateTimeout
import time
from datetime import date, datetime

@require_permission("LIST", Timetracking)
def overview(request):
    updateTimeout(request)
    timetrackings = Timetracking.objects.filter(creator=Core.current_user())

    sumHours = 0
    for time in timetrackings:
        sumHours += time.hours_worked

    return render_with_request(request, 'timetracking/list.html',
                               {'title': 'Timeføringer', 'timetrackings': timetrackings, 'sumHours':sumHours})

@require_permission("CREATE", Timetracking)
def add(request):
    return form(request)


@require_permission("EDIT", Timetracking, "id")
def edit(request, id):
    return form(request, id)


@require_permission("DELETE", Timetracking, "id")
def delete(request, id):
    Timetracking.objects.get(id=id).delete()
    return redirect(overview)

def addAjax(request):
    return

@require_permission("CREATE", Timetracking)
def addTypeOfWork(request):
    instance = TypeOfTimeTracking()
    msg = "Velykket lagt til ny type arbeid"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = TypeOfTimeTrackingForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            request.message_success(request, msg)

            #Redirects after save for direct editing
            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    (escape(o._get_pk_val()), escape(o)))
    else:
        form = TypeOfTimeTrackingForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Typer arbeid', 'form': form})

@require_permission("LIST", Timetracking)
def calendar(request):
    timetrackings = Timetracking.objects.all()

    instance = Timetracking()
    form = TimetrackingForm(request.POST, instance=instance)

    return render_with_request(request, "timetracking/calendar.html", {'title': 'Timeregistrering',
                                                                       'timetrackings': timetrackings,
                                                                       'form': form, })

@login_required()
def ajaxEditCalendar(request):
    from django.utils import simplejson

    timeTrackingID = request.GET.get("timeTrackingID")

    if timeTrackingID:
        t = Timetracking.objects.get(id=timeTrackingID)
    else:
        t = Timetracking()

    o = Order.objects.get(id=1)
    b = TypeOfTimeTracking.objects.get(id=1)

    time_start = "%s" % request.GET.get("time_start")
    time_stop = "%s" % request.GET.get("time_end")

    datAe = request.GET.get("date")
    tempDate = time.strptime(datAe, "%d.%m.%Y")
    k = date(tempDate[0], tempDate[1], tempDate[2])

    t.hours_worked = 1
    t.typeOfWork = b
    t.order = o
    t.date = k
    t.time_start = time_start
    t.time_end = time_stop

    t.save()

    data = simplejson.dumps({'id': t.id})

    return HttpResponse(data)


@login_required()
def form (request, id=False):
    if id:
        instance = get_object_or_404(Timetracking, id=id, deleted=False)
        msg = "Velykket endret timeføring"
    else:
        instance = Timetracking()
        msg = "Velykket lagt til nytt timeføring"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = TimetrackingForm(request.POST, instance=instance)

        if form.is_valid():

            date = request.POST['date']

            start = time.strptime("%s %s"%(date,request.POST['time_start']),"%d.%m.%Y  %H:%M")
            end = time.strptime("%s %s"%(date,request.POST['time_end']),"%d.%m.%Y  %H:%M")

            start_t = time.mktime(start)
            end_t = time.mktime(end)

            clockValid = True

            if start_t > end_t:
                request.message_error("Du kan ikke slutte før du begynte")
                clockValid = False

            hoursWorked = calculateHoursWorked(request, start_t, end_t)

            if hoursWorked <= 0:
                clockValid = False

            if clockValid:
                o = form.save(commit=False)
                o.hours_worked = hoursWorked
                o.save()
                request.message_success(msg)

                #Redirects after save for direct editing
                return overview(request)


    else:
        form = TimetrackingForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Timeføring', 'form': form})