# -*- coding: utf-8 -*-
from django.shortcuts import  redirect
from django.contrib.auth.decorators import login_required
from forms import *
from core.shortcuts import *
from django.contrib import messages
from django.utils.html import escape
from core.views import updateTimeout
import time
from datetime import date

@login_required
def overview(request):
    updateTimeout(request)
    timetrackings = Timetracking.objects.for_user()
    return render_with_request(request, 'timetracking/list.html',
                               {'title': 'Timeføringer', 'timetrackings': timetrackings})

@login_required
def add(request):
    return form(request)


@login_required
def edit(request, id):
    return form(request, id)


@login_required
def delete(request, id):
    Timetracking.objects.get(id=id).delete()
    return redirect(overview)

def addAjax(request):
    return

@login_required
def addTypeOfWork(request):
    instance = TypeOfTimeTracking()
    msg = "Velykket lagt til ny type arbeid"

    #Save and set to active, require valid form
    if request.method == 'POST':
        form = TypeOfTimeTrackingForm(request.POST, instance=instance)
        if form.is_valid():
            o = form.save(commit=False)
            o.save()
            messages.success(request, msg)

            #Redirects after save for direct editing
            return HttpResponse(
                    '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %\
                    (escape(o._get_pk_val()), escape(o)))
    else:
        form = TypeOfTimeTrackingForm(instance=instance)

    return render_with_request(request, "simpleform.html", {'title': 'Typer arbeid', 'form': form})


@login_required
def calculateHoursWorked(request, start, end):
    diff = 0
    start = time.strptime("2010 " + start, "%Y %H:%M")
    end = time.strptime("2010 " + end, "%Y %H:%M")
    diff = time.mktime(end) - time.mktime(start)

    if diff < 1:
        mg = "Sjekk klokkeslettene en gang til"
        messages.error(request, mg)

    diff = str(diff / 3600)

    return diff


@login_required
def calendar(request):
    timetrackings = Timetracking.objects.for_user()

    instance = Timetracking()
    form = TimetrackingForm(request.POST, instance=instance)

    return render_with_request(request, "timetracking/calendar.html", {'title': 'Timeregistrering',
                                                                       'timetrackings': timetrackings,
                                                                       'form': form, })

@login_required
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


@login_required
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

        if request.POST['time_start'] > request.POST['time_end']:
            messages.error(request, "Du kan ikke slutte før du begynte")

        elif form.is_valid():
            clockValid = True
            hoursWorked = calculateHoursWorked(request, request.POST['time_start'], request.POST['time_end'])
            if hoursWorked == 0:
                clockValid = False

            if clockValid:
                o = form.save(commit=False)
                o.hours_worked = hoursWorked
                o.save()
                messages.success(request, msg)

                #Redirects after save for direct editing
                return overview(request)


    else:
        form = TimetrackingForm(instance=instance)

    return render_with_request(request, "form.html", {'title': 'Timeføring', 'form': form})